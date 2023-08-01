# -*- coding: utf-8 -*-
from odoo import models, fields
import datetime
import json
import logging
import requests

REQUEST_TOKEN_URL = "https://login.etrusted.com/oauth/token"
INVITES_API_URL = "https://api.etrusted.com/invites"

_logger = logging.getLogger(__name__)


class TrustedShopsApi(models.Model):
    _name = "trusted.shops.api"

    def _request(self, payload, trusted_shops_data):
        """
        Send a request to the TrustedShops API.
        """
        access_token = self._get_access_token(trusted_shops_data)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }
        # request = requests.post(INVITES_API_URL, data=payload, headers=headers)
        try:
            request.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.debug("TrustedShops API request failed: %s", e)
            raise

        response = request.json()
        return response

    def _get_access_token(self, trusted_shops_data):
        """
        Get the access token from the TrustedShops API.
        """
        payload = {
            "grant_type": "client_credentials",
            "client_id": trusted_shops_data.get("trusted_shops_client_id"),
            "client_secret": trusted_shops_data.get("trusted_shops_client_secret"),
            "audience": "https://api.etrusted.com",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        request = requests.post(REQUEST_TOKEN_URL, data=payload, headers=headers)
        try:
            request.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.debug("TrustedShops API request failed: %s", e)
            raise

        response = request.json()
        return response["access_token"]

    def post_invite(self, picking):
        """
        Post an invite to the TrustedShops API.
        """
        payload = ""
        sale_order_created_date_datetime = datetime.datetime.strptime(
            fields.Datetime.to_string(picking.sale_id.create_date), "%Y-%m-%d %H:%M:%S"
        )
        datetime_now = datetime.datetime.now()

        trusted_shops_data = {
            "trusted_shops_client_id": picking.website_id.trusted_shops_client_id,
            "trusted_shops_client_secret": picking.website_id.trusted_shops_client_secret,
        }

        country_delay = self.env["trusted.shops.country.delay"].search(
            [
                ("country_id.code", "=", picking.partner_id.country_id.code),
                ("website_id", "=", picking.website_id.id),
            ]
        )
        if len(country_delay) > 0:
            time_delay = int(country_delay.delay)
        else:
            time_delay = int(
                picking.website_id.trusted_shops_standard_timedelay_invitation
            )

        preferred_sendtime = datetime_now + datetime.timedelta(days=time_delay)

        customer_language_code = picking.sale_id.partner_id.lang
        trusted_shops_channel_id = (
            self.env["trusted.shops"]
            .search(
                [
                    ("language_id.code", "=", customer_language_code),
                    ("website_id", "=", picking.website_id.id),
                ]
            )
            .trusted_shops_id
        )

        locale = (
            customer_language_code if customer_language_code != "en_US" else "en_150"
        )

        payload = json.dumps(
            {
                "channel": {"id": trusted_shops_channel_id, "type": "user_defined"},
                "system": "Odoo",
                "systemVersion": "1.0.0",
                "invites": [
                    {
                        "questionnaireTemplate": {
                            "id": "tpl-qst-baaec16a-7fd6-4815-b119-9aadea3cf986"
                        },
                        "template": {
                            "id": "tpl-inv-f0232e18-bdd4-4465-9de5-03a6f36abb46"
                        },
                        "customer": {
                            "firstName": picking.sale_id.partner_id.name,
                            "email": picking.sale_id.partner_id.email,
                        },
                        "locale": locale,
                        "transaction": {
                            "reference": picking.sale_id.name,
                            "date": sale_order_created_date_datetime.isoformat("T")
                            + "Z",
                        },
                        "preferredSendTime": preferred_sendtime.isoformat("T") + "Z",
                    }
                ],
            }
        )

        self._request(payload, trusted_shops_data)
        return True
