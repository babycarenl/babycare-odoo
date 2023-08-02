# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TrustedShopsCountryDelay(models.Model):
    _name = "trusted.shops.country.delay"
    _rec_name = "country_id"

    country_id = fields.Many2one("res.country", "Country", required=True)
    delay = fields.Integer(string="Delay", required=True)
    website_id = fields.Many2one("website")

    @api.constrains("website_id", "country_id")
    def _check_unique_combination(self):
        for record in self:
            existing_record = self.search(
                [
                    ("website_id", "=", record.website_id.id),
                    ("country_id", "=", record.country_id.id),
                ]
            )
            if len(existing_record) > 1:
                raise ValidationError(
                    "This combination of website and country already exists."
                )
