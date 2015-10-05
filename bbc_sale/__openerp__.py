# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Opener B.V. (<https://opener.am>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Babycare Sales customizations",
    "category": "Sale",
    "version": "1.0",
    "author": "Opener B.V.",
    "website": 'https://opener.am',
    "depends": [
        'sale_stock',
        'point_of_sale',
        'purchase',
    ],
    'data': [
        'views/templates.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
        'views/stock_picking.xml',
        'data/ir_cron.xml',
    ],
}