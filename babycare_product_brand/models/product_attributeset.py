# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ProductAttributeSet(models.Model):
    _name = 'product.attributeset'
    name = fields.Char('Product Attribute Set', required=True, translate=True)
    options_ids = fields.One2many(
        'product.options',
        'attributeset_id',
        'Options'
    )

    @api.multi
    def unlink(self):
        if self.env['product.options'].search(
                [('attributeset_id', 'in', self.ids)]):
            raise UserError(
                (
                    'The operation cannot be completed:\n'
                    'You trying to delete an attribute set'
                    ' with a reference on a product option.'
                )
            )
        return super(ProductAttributeSet, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The Name of the Product Attribute Set must be unique"
        )
    ]
