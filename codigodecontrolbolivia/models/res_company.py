# -*- coding: utf-8 -*-.
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError

class Actividad(models.Model):
	_name = 'res.actividad'
	_description = 'ActividadEconomica'
	
	
	company_id = fields.Many2one('res.company', string="Compañía")
	name = fields.Char(string='Actividad Economica')


class Company(models.Model):
	_inherit = 'res.company'
	
	company_registry  = fields.One2many('res.actividad','company_id', string="Actividad Economica")
    
    
