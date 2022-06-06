# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'
    
    razonsocial = fields.Char(string='Razon Social', readonly=False, store=True, compute='_nombre_a_razon_social')
	
    @api.depends('name')
    def _nombre_a_razon_social(self):
        for r in self:	
            if not r.razonsocial :
                r.razonsocial =  r.name