{
    'name': 'UPS export to CSV',
    'version': '8.0.1.0',
    'category': '',
    'summary': 'Export deliveries to a CSV file to import in UPS Worldship',
    'author':
        'codeNext',
    'license': 'LGPL-3',
    'depends': [
        'base', 'stock',
    ],
    'data': [
        'views/sftp_view.xml',
        'views/export_ups_wizard.xml',
    ],
    'installable': True,
}
