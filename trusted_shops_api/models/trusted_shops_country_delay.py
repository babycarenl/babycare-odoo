# coding: utf-8
from openerp import fields, models


class TrustedShopsCountryDelay(models.Model):
    _name = 'trusted.shops.country.delay'

    country_id = fields.Many2one('res.country', 'Country')
    delay = fields.Integer(string='Delay', required=True)
