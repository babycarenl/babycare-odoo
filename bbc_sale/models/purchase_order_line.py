# -*- coding: utf-8 -*-
from openerp import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_state = fields.Selection(
        related='product_id.state')
    virtual_available = fields.Float(
        related='product_id.virtual_available')
    website_published = fields.Boolean(
        related='product_id.website_published')
    is_component = fields.Boolean(
        related='product_id.is_component')
    published_or_part = fields.Boolean(
        'Site', compute='_compute_published_or_part',
        help='Is published or is part of a configurable product')

    @api.multi
    def onchange_product_id(
            self, pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False,
            state='draft'):
        res = super(PurchaseOrderLine, self).onchange_product_id(
            pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=date_order, fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, name=name, price_unit=price_unit,
            state=state)
        if product_id and res.get('value'):
            product = self.env['product.product'].browse(product_id)
            res['value'].update(
                virtual_available=product.virtual_available,
                product_state=product.state)
        return res

    @api.depends('product_id', 'website_published', 'is_component')
    def _compute_published_or_part(self):
        """ Compute if a product is website_published or is_component,
        and if it is, set published_or_part to True """
        for product in self:
            if (product.website_published or product.is_component):
                product.published_or_part = True
            else:
                product.published_or_part = False
