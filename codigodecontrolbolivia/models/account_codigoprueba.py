# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools

class account_codigoprueba(models.Model):
    #Hereda todo y modifica
    _inherit = 'account.move'
    #Crea los siguientes campos
    autorizacion =  fields.Char(string='Limite de emision', store=True, readonly=False)	
    
    numfactura =  fields.Char(string='Limite de emision', store=True, readonly=False)	
    nit = fields.Char(string='Nit', store=True, readonly=False, compute='_compute_nit')
    fecha = fields.Char()
    total = fields.Char()
    llave = fields.Char()
    cc = fields.Char()
    ok = fields.Char()
    codigodecontrol = fields.Char(string='Codigo de Control', store=True, readonly=False)
    
