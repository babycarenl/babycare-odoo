# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    published_or_part = fields.Boolean(
        "Site",
        compute="_compute_published_or_part",
        help="Is published or is part of a configurable product",
    )
    used_in_bom_count = fields.Integer(related="product_id.used_in_bom_count")
    website_published = fields.Boolean(related="product_id.website_published")

    @api.depends("product_id", "website_published")
    def _compute_published_or_part(self):
        """Compute if a product is website_published or is_component,
        and if it is, set published_or_part to True"""
        for product in self:
            if product.website_published or product.used_in_bom_count > 0:
                product.published_or_part = True
            else:
                product.published_or_part = False
