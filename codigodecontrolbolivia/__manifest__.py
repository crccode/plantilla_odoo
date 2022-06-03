# -*- coding: utf-8 -*-
{
    'name': "Codigo de Control Bolivia",
	
    'summary': """
        Modulo de Facturación para Bolivia, 
        Codigo de Control, QR, Total a Texto""",

    'sequence': 1,

    'description': """
        Este Modulo de Facturación para Bolivia, configura el Código de Control, Codigo QR, Total a Texto Literal.
        Algunas modificaciones previas hay que realizar antes de poder facturar de manera computarizada.
		El Modulo se encuentra en un Etapa Inicial Beta, cualquier Error por favor reportarlo, las Sugerencias son bienvenidas.
		La documentación y las nuevas versiones estarán disponibles en https://github.com/miguelbelmonte/Odoo11_codigodecontrolbolivia		
    """,

    'author': "Miguel Belmonte",
    'support': "miguel@buenisimoyriquisimo.com",

    'category': 'Accounting',
    'version': '14.0.2',
    'depends': ['base', 'account', 'contacts'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/account_invoice.xml',
        'views/codigoprueba.xml',
        'views/account_journal_cc.xml',
		'views/res_company.xml',
        'report/invoice_report_qr.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'qweb': [
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}