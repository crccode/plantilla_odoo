# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Module(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def get_module_installation_status(self, domain=None, fields=None):
        record = self.sudo().search_read(domain, fields)
        if len(record) == 0:
            return False
        else:
            if record[0]['state'] != 'installed':
                return False
            else:
                return True
