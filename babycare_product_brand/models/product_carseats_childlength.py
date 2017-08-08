# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ProductCarSeatsChildLength(models.Model):
    _name = 'product.carseats.childlength'
    name = fields.Char('Child Length', required=True, translate=True)

    @api.multi
    def unlink(self):
        product_ids = self.env['product.product'].search([(
            'product_carseats_childlength_id', 'in', self.ids
        )])
        if product_ids:
            raise UserError(
                (
                    'The operation cannot be completed:\n'
                    'You trying to delete a record with'
                    ' a reference on a product variant.'
                )
            )
        return super(ProductCarSeatsChildLength, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The name of the record must be unique"
        )
    ]
