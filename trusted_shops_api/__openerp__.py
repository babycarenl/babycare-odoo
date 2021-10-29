{
    "name": "Trusted Shops Integration",
    "summary": "Integrate Trusted Shops with Odoo",
    "version": "8.0.0.1.0",
    "author": "codeNext",
    "website": "https://codenext.nl",
    "depends": [
        'base',
        'stock'
    ],
    "data": [
        'views/trusted_shops_api_view.xml',
        'views/stock_picking.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3',
}
