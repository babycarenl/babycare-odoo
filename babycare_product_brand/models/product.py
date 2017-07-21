# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_color_id = fields.Many2one(
        'product.color',
        string='Color',
        help='Select a color for this product',
        related='product_variant_ids.product_color_id',
        readonly=True
    )
    product_options_ids = fields.Many2many(
        'product.options',
        string='Options',
        help='Select options for this product',
        ondelete='restrict'
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_color_id = fields.Many2one(
        'product.color',
        string='Color',
        help='Select a color for this product'
    )

    @api.multi
    def open_magento_synchronization(self):
        """ Opens a form to synchronize
        attributes from Odoo to Magento """
        view_ref = self.env['ir.model.data'].get_object_reference(
            'mob_brand', 'magento_attribute_sync_form'
        )
        view_id = view_ref[1] if view_ref else False
        res = {
            'type': 'ir.actions.act_window',
            'name': 'Magento Synchronization',
            'res_model': 'magento.synchronization',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'self',
            'flags': {'action_buttons': False},
        }
        return res
