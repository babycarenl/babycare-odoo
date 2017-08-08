# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ProductClothesSeason(models.Model):
    _name = 'product.clothes.season'
    name = fields.Char('Season', required=True, translate=True)

    @api.multi
    def unlink(self):
        product_ids = self.env['product.product'].search([(
            'product_clothes_season_id', 'in', self.ids
        )])
        if product_ids:
            raise UserError(
                (
                    'The operation cannot be completed:\n'
                    'You trying to delete a record with'
                    ' a reference on a product variant.'
                )
            )
        return super(ProductClothesSeason, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The name of the record must be unique"
        )
    ]
