# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    has_trusted_shops = fields.Boolean(
        "Trusted Shops",
        compute="_compute_has_trusted_shops",
        inverse="_inverse_has_trusted_shops",
    )

    trusted_shops_client_id = fields.Char(
        "Client ID",
        help="Client ID from Trusted Shops",
        related="website_id.trusted_shops_client_id",
        readonly=False,
    )

    trusted_shops_client_secret = fields.Char(
        "Client Secret",
        help="Client Secret from Trusted Shops",
        related="website_id.trusted_shops_client_secret",
        readonly=False,
    )

    standard_timedelay_invitation = fields.Integer(
        "Standard Time Delay Invitation",
        help="Standard time delay for sending invitations",
        related="website_id.trusted_shops_standard_timedelay_invitation",
        default=7,
        readonly=False,
    )

    @api.depends("website_id")
    def _compute_has_trusted_shops(self):
        for config in self:
            config.has_trusted_shops = bool(config.trusted_shops_client_id)

    def _inverse_has_trusted_shops(self):
        for config in self:
            if config.has_trusted_shops:
                continue
            config.trusted_shops_client_id = False
            config.trusted_shops_client_secret = False
            config.standard_timedelay_invitation = False

    def action_trusted_shops(self):
        return {
            "name": "Trusted Shops",
            "view_mode": "tree,form",
            "res_model": "trusted.shops",
            "type": "ir.actions.act_window",
            "domain": [("website_id.id", "=", self.website_id.id)],
            "context": {"default_website_id": self.website_id.id},
        }

    def action_trusted_shops_country_delay(self):
        return {
            "name": "Trusted Shops Country Delay",
            "view_mode": "tree,form",
            "res_model": "trusted.shops.country.delay",
            "type": "ir.actions.act_window",
            "domain": [("website_id.id", "=", self.website_id.id)],
            "context": {"default_website_id": self.website_id.id},
        }
