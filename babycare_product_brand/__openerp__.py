{
    'name': 'Product Attribute Manager',
    'version': '8.0.1.0',
    'category': 'Product',
    'summary': 'Add attributes to products',
    'author':
        'Wytze Jan Riedstra, NetAndCo, Akretion, Prisnet Telecommunications SA'
        ', MONK Software, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'depends': [
        'product_brand',
        'mob_extra_images',
    ],
    'data': [
        'views/product.xml',
        'views/product_attributeset.xml',
        'views/product_color.xml',
        'views/product_options.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'post_load': 'post_load',
}
