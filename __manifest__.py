# -*- coding: utf-8 -*-
{
    'name': 'CLBCL',
    'version': '2.0.0',
    'summary': 'CLBCL',
    'sequence': -100,
    'description': """CLBCL""",
    'category': 'Tutorials',
    'author': 'Kelvin',
    'maintainer': 'Kelvin',
    'website': 'https://www.odoomates.tech',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'mail',
        'website_slides',
        'hr',
        'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/club_view.xml',
        'views/club_area_view.xml',
        'views/club_user_view.xml',
        'views/sale_order_view.xml',
        'views/club_partner_product_view.xml',
        'views/product_category_view.xml',
        'views/product_template_view.xml',
        'views/product_product_view.xml',
        'views/voucher_view.xml',
        'views/bank_info_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
