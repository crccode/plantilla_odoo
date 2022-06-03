# -*- coding: utf-8 -*-

from .CC import codcontr
from .TotalATexto import totalliteral
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
import time

class AccountMove(models.Model):
	#Hereda todo y modifica
	_inherit = 'account.move'
	
	#Crea los siguientes campos
	limiteemision = fields.Char(string='Limite de emision', store=False, readonly=True, compute='_compute_limite_emision')	
	codigodecontrol = fields.Char(string='Codigo de Control', store=True, readonly=False, compute='_codigo_de_control')
	nit = fields.Char(string='Nit', store=True, readonly=False, compute='_compute_nit')
	razonsocial = fields.Char(string='Razon Social', store=True, readonly=False, compute='_compute_nit', website_form_blacklisted=False)
	totaltexto = fields.Char(string='Son :', store=False, readonly=True, compute='_compute_literal')
	autorizacion = fields.Char(string='Autorizacion #', store=True, readonly=False, compute='_autorizacion')

	
	@api.depends('amount_total')
	def _compute_literal(self):
		for r in self:
			r.totaltexto =  totalliteral(r.amount_total, r.currency_id.name)
	
    #,'vat', 'razonsocial')
	@api.depends('partner_id') 
	def _compute_nit(self):	
		for r in self:
			#if r.nit is None:
				r.nit = r.partner_id.vat
			#if r.razonsocial is None:
				r.razonsocial = r.partner_id.razonsocial
			
	@api.depends('journal_id.limiteemision')
	def _compute_limite_emision(self):
		for r in self:
			if r.journal_id.limiteemision :
				r.limiteemision = time.strftime('%d/%m/%Y', time.strptime(str(r.journal_id.limiteemision),'%Y-%m-%d'))
				
	@api.depends('journal_id.autorizacion','state')
	def _autorizacion(self): 
		for r in self:
			if r.journal_id.autorizacion and r.journal_id.type == 'sale' :
				r.autorizacion = r.journal_id.autorizacion				
				
	@api.depends('state')
	def _codigo_de_control(self): 
		for r in self:
			if r.name and r.sequence_prefix and r.journal_id.autorizacion and r.invoice_date and r.amount_total and r.journal_id.llave and r.state=='posted':
				numfactura = r.name.replace(r.sequence_prefix,'')
				r.codigodecontrol = codcontr(r.autorizacion, numfactura, r.nit, r.invoice_date, r.amount_total, r.journal_id.llave)