# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TrustedShops(models.Model):
    _name = "trusted.shops"
    _rec_name = "trusted_shops_id"

    trusted_shops_id = fields.Char(string="Trusted Shops ID", required=True)
    website_id = fields.Many2one("website")
    language_id = fields.Many2one(
        "res.lang", string="Language", readonly=False, required=True
    )

    @api.onchange("website_id")
    def _onchange_website_id(self):
        if self.website_id:
            return {
                "domain": {
                    "language_id": [("id", "in", self.website_id.language_ids.ids)]
                }
            }
        else:
            return {"domain": {"language_id": []}}

    @api.constrains("website_id", "language_id")
    def _check_unique_combination(self):
        for record in self:
            existing_record = self.search(
                [
                    ("website_id", "=", record.website_id.id),
                    ("language_id", "=", record.language_id.id),
                ]
            )
            if len(existing_record) > 1:
                raise ValidationError(
                    "This combination of website and language already exists."
                )
