# -*- coding: utf-8 -*-
{
    'name': 'PWA for Odoo',
    'version': '14.0.1.0.0',
    'summary': '''
    PWA features for Odoo
    | PWA Frontend
    | PWA Backend
    | Progressive Web Application
    | PWApplication from website
    | Add to Home Screen PWA
    ''',
    'category': 'Website, Extra Tools',
    'author': 'XFanis',
    'support': 'odoo@xfanis.dev',
    'website': 'https://xfanis.dev',
    'license': 'OPL-1',
    'price': 10,
    'currency': 'EUR',
    'description':
        """
PWA for Odoo Backend and Frontend
=================================
Progressive Web Application for Odoo Backend and Frontend!
PWA provides an application experience to the ERP system users.
        """,
    'data': [
        'security/ir.model.access.csv',
        'data/pwa_categories.xml',
        'views/assets.xml',
        'views/pwa_manifest.xml',
        'views/offline_page.xml',
    ],
    'depends': [],
    'qweb': ['static/src/xml/*.xml'],
    'images': [
        'static/description/xf_pwa.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
