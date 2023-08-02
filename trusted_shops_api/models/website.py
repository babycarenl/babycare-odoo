# -*- coding: utf-8 -*-
from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    trusted_shops_client_id = fields.Char("Client ID")
    trusted_shops_client_secret = fields.Char("Client Secret")
    trusted_shops_standard_timedelay_invitation = fields.Integer(
        "Standard Time Delay Invitation"
    )
