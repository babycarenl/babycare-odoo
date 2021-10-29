# coding: utf-8
from openerp import models
import datetime
import json
import logging
import requests

REQUEST_TOKEN_URL = 'https://login.etrusted.com/oauth/token'
INVITES_API_URL = 'https://api.etrusted.com/invites'

_logger = logging.getLogger(__name__)


class TrustedShopsApi(models.Model):
    _name = 'trusted.shops.api'

    def _request(self, payload):
        """
        Send a request to the TrustedShops API.
        """
        access_token = self._get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        try:
            request = requests.post(INVITES_API_URL, data=payload, headers=headers)
            response = request.json()
            return response
        except requests.exceptions.RequestException as e: 
            _logger.debug("TrustedShops API request failed with code: %r, msg: %r, content: %r",
                          e.code, e.msg, e.fp.read())
            raise
    
    def _get_access_token(self):
        """
        Get the access token from the TrustedShops API.
        """
        params = self.env['ir.config_parameter']
        client_id = params.get_param('trusted_shops_api.trusted_shops_api_client_id')
        client_secret = params.get_param('trusted_shops_api.trusted_shops_api_client_secret')
        try:
            payload = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "audience": "https://api.etrusted.com"
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            request = requests.post(REQUEST_TOKEN_URL, data=payload, headers=headers)
            response = request.json()
            return response['access_token']
        except requests.exceptions.RequestException as e: 
            _logger.debug("TrustedShops API request failed with code: %r, msg: %r, content: %r",
                          e.code, e.msg, e.fp.read())
            raise
    
    def post_invite(self, picking):
        """
        Post an invite to the TrustedShops API.
        """
        params = self.env['ir.config_parameter']
        default_timedelay_invitation = int(params.get_param(
            'trusted_shops_api.default_timedelay_invitation'))

        sale_order_created_date_datetime = datetime.datetime.strptime(
            picking.sale_id.create_date, '%Y-%m-%d %H:%M:%S')
        datetime_now = datetime.datetime.now()
        preferred_sendtime = datetime_now + datetime.timedelta(days = default_timedelay_invitation)

        magento_shop_code = picking.sale_id.wk_shop.code
        trusted_shops_channel_id = self.env['trusted.shops'].search([
            ('language', '=', magento_shop_code)
        ]).trusted_shops_id
        
        payload = json.dumps({
            "channel": {
                "id": trusted_shops_channel_id,
                "type": "user_defined"
            },
            "system": "Odoo",
            "systemVersion": "1.0.0",
            "invites": [
                {
                "questionnaireTemplate": {
                    "id": "tpl-qst-1605077d-f768-422d-8fad-809f93d7a18f"
                },
                "template": {
                    "id": "tpl-inv-f52b110f-ee37-4305-8cec-ba2d5ab1db8f"
                },
                "customer": {
                    "firstName": picking.sale_id.partner_id.name,
                    "email": picking.sale_id.partner_id.email,
                },
                "locale": picking.sale_id.partner_id.lang,
                "transaction": {
                    "reference": picking.sale_id.name,
                    "date": sale_order_created_date_datetime.isoformat("T") + "Z"
                },
                "preferredSendTime": preferred_sendtime.isoformat("T") + "Z",
                }
            ]
        })
        
        self._request(payload)
        return True
