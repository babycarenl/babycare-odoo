# coding: utf-8
from openerp import fields, models


class TrustedShops(models.Model):
    _name = 'trusted.shops'
    
    trusted_shops_id = fields.Char()
    language = fields.Char()
