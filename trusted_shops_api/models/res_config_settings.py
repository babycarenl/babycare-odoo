# coding: utf-8
from openerp import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    trusted_shops_api_client_id = fields.Char(
        string='Client ID',
        help='Client ID from Trusted Shops API',
        required=True)
    trusted_shops_api_client_secret = fields.Char(
        string='Client Secret',
        help='Client Secret from Trusted Shops API',
        required=True)
    default_timedelay_invitation = fields.Integer(
        string='Default Time Delay Invitation',
        help='Default time delay for sending invitations',
        default=7,
        required=True)

    @api.multi
    def get_default_trusted_shops_values(self):
        ir_config_parameter = self.env['ir.config_parameter']
        return {
            'trusted_shops_api_client_id': ir_config_parameter.get_param(
                'trusted_shops_api.trusted_shops_api_client_id') or '',
            'trusted_shops_api_client_secret': ir_config_parameter.get_param(
                'trusted_shops_api.trusted_shops_api_client_secret') or '',
            'default_timedelay_invitation': int(ir_config_parameter.get_param(
                'trusted_shops_api.default_timedelay_invitation')) or 7
        }

    @api.multi
    def set_trusted_shops_values(self):
        ir_config_parameter = self.env['ir.config_parameter']
        ir_config_parameter.set_param(
            'trusted_shops_api.trusted_shops_api_client_id', self.trusted_shops_api_client_id)
        ir_config_parameter.set_param(
            'trusted_shops_api.trusted_shops_api_client_secret', self.trusted_shops_api_client_secret)
        ir_config_parameter.set_param(
            'trusted_shops_api.default_timedelay_invitation', self.default_timedelay_invitation)
