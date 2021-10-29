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
    trusted_shops_ids = fields.Many2many(
        'trusted.shops',
        string='Trusted Shops')

    @api.multi
    def get_default_trusted_shops_values(self):
        trusted_shops_ids = self.env['ir.values'].get_default(
            'res.config.settings',
            'trusted_shops_ids')
        ir_config_parameter = self.env['ir.config_parameter']
        return {
            'trusted_shops_ids': trusted_shops_ids,
            'trusted_shops_api_client_id': ir_config_parameter.get_param(
                'trusted_shops_api.trusted_shops_api_client_id') or '',
            'trusted_shops_api_client_secret': ir_config_parameter.get_param(
                'trusted_shops_api.trusted_shops_api_client_secret') or ''
        }

    @api.multi
    def set_trusted_shops_values(self):
        self.env['ir.values'].set_default(
            'res.config.settings',
            'trusted_shops_ids',
            self.trusted_shops_ids.ids)
        ir_config_parameter = self.env['ir.config_parameter']
        ir_config_parameter.set_param(
            'trusted_shops_api.trusted_shops_api_client_id', self.trusted_shops_api_client_id)
        ir_config_parameter.set_param(
            'trusted_shops_api.trusted_shops_api_client_secret', self.trusted_shops_api_client_secret)
