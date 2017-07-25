# -*- coding: utf-8 -*-
from openerp import models, fields


class ProductAttributeSet(models.Model):
    _name = 'product.attributeset'
    name = fields.Char('Product Attribute Set', required=True, translate=True)
    options_ids = fields.One2many(
        'product.options',
        'attributeset_id',
        'Options'
    )

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The Name of the Product Attribute Set must be unique"
        )
    ]
