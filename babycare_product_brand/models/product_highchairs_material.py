# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ProductHighChairsMaterial(models.Model):
    _name = 'product.highchairs.material'
    name = fields.Char('Material', required=True, translate=True)

    @api.multi
    def unlink(self):
        product_ids = self.env['product.product'].search([(
            'product_highchairs_material_id', 'in', self.ids
        )])
        if product_ids:
            raise UserError(
                (
                    'The operation cannot be completed:\n'
                    'You trying to delete a record with'
                    ' a reference on a product variant.'
                )
            )
        return super(ProductHighChairsMaterial, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The name of the record must be unique"
        )
    ]
