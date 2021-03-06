# coding: utf-8
# Copyright (C) 2015 - 2017 Opener B.V. <https://opener.amsterdam>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Babycare Stock customizations",
    "category": "Stock",
    "version": "1.0",
    "author": "Opener B.V.",
    "website": 'https://opener.am',
    "depends": [
        # NB keep the dependency on stock even though delivery already depends
        # on stock, because it seems like the webclient does not do transitive
        # dependencies...
        'stock',
        'delivery',
        'bbc_sale',
        'mob_tracking',
        'website_sale_options',
    ],
    'data': [
        'views/assets.xml',
        'views/product.xml',
        'views/stock_move.xml',
        'views/stock_picking.xml',
        'data/ir_cron.xml',
        'report/report_return_form_outgoing_delivery_de.xml',
        'report/report_return_form_outgoing_delivery_en.xml',
        'report/report_return_form_outgoing_delivery_nl.xml',
        'report/report_shipping_information_de.xml',
        'report/report_shipping_information_en.xml',
        'report/report_shipping_information_nl.xml',
        'report/bbc_stock_reports.xml',
    ],
    'qweb': ['static/src/xml/picking.xml'],
}
