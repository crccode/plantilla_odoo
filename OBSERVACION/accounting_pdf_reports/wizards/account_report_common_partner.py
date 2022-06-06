# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountingCommonPartnerReport(models.TransientModel):
    _name = 'account.common.partner.report'
    _description = 'Account Common Partner Report'
    _inherit = "account.common.report"

    result_selection = fields.Selection([('customer', 'Receivable Accounts'),
                                         ('supplier', 'Payable Accounts'),
                                         ('customer_supplier', 'Receivable and Payable Accounts')
                                         ], string="Partner's", required=True, default='customer')
    abc = fields.Selection([('all', '1+2'), ('a', '1'),
                                        ('b', '2'), ],
                                       string='Centro de Costos', required=True, default='a')


    def pre_print_report(self, data):
        data['form'].update(self.read(['result_selection'])[0])
        return data
