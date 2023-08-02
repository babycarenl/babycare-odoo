# -*- coding: utf-8 -*-

{
    "name": "Trusted Shops Integration",
    "version": "16.0.0.1.0",
    "summary": "Integrate Trusted Shops with Odoo",
    "website": "https://www.codenext.nl",
    "author": "codeNext",
    "depends": ["base", "stock", "website", "website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/trusted_shops_views.xml",
        "views/res_config_settings_views.xml",
        "views/stock_view.xml",
    ],
}
