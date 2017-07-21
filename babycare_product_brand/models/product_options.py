# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ProductOptions(models.Model):
    _name = 'product.options'
    _rec_name = 'display_name'
    name = fields.Char('Product Options', required=True, translate=True)
    attributeset_id = fields.Many2one(
        'product.attributeset',
        'Attribute',
        required=True
    )
    display_name = fields.Char(
        'Display Name',
        store=True,
        translate=True,
        compute='_get_display_name'
    )

    @api.multi
    @api.depends('name', 'attributeset_id.name')
    def _get_display_name(self):
        names = [self.attributeset_id.name, self.name]
        self.display_name = ' / '.join(filter(None, names))

    @api.one
    def unlink(self):
        product_ids = self.env['product.product'].search([(
            'product_options_ids', 'in', self.ids
        )])
        if product_ids:
            raise UserError(
                (
                    'The operation cannot be completed:\n'
                    'You trying to delete a product option'
                    ' with a reference on a product variant.'
                )
            )
        return super(ProductOptions, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The Name of the Product Option must be unique"
        )
    ]
