# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ProductColor(models.Model):
    _name = 'product.color'
    name = fields.Char('Color Name', required=True, translate=True)

    @api.multi
    def unlink(self):
        product_ids = self.env['product.product'].search([(
            'product_color_id', 'in', self.ids
        )])
        if product_ids:
            raise UserError(
                (
                    'The operation cannot be completed:\n'
                    'You trying to delete a product color with'
                    ' a reference on a product variant.'
                )
            )
        return super(ProductColor, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The Name of the Product Color must be unique"
        )
    ]
