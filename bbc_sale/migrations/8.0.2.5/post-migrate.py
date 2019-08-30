# coding: utf-8
from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """ Set weight equal to weight_net if weight is null or 0 """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.cr.execute(
        """ UPDATE product_template
        SET weight = weight_net
        WHERE weight_net > 0
            AND (weight IS NULL OR weight = 0) """)
