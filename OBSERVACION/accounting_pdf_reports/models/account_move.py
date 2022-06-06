# -*- coding: utf-8 -*-

from odoo import models, api, _, fields


class AccountMove(models.Model):
	#Hereda todo y modifica
	_inherit = 'account.move'
	
	#Crea los siguientes campos
	a = fields.Boolean(string='Centro de Costos :', store=True, readonly=False, compute='_move_id_a_journal')
	extra_sequence = fields.Char(string='Secuencia Mensual', readonly=True, store=True, states={'draft': [('readonly', False)]}, compute='_extra_sequence')
	payment_type = fields.Selection(related='payment_id.payment_type', store=True, readonly=True)
	is_internal_transfer = fields.Boolean(related='payment_id.is_internal_transfer', store=True, readonly=True)


	@api.depends('journal_id.a')
	def _move_id_a_journal(self): 
		for r in self:
			if not r.extra_sequence:
				r.a = r.journal_id.a
			
	@api.depends('state')
	def _extra_sequence(self): 
		for r in self:
			if r.state=='posted' and (not r.extra_sequence or r.extra_sequence=='') and r.a :
				if r.payment_type == 'inbound' and not r.is_internal_transfer :
					r.extra_sequence=self.env['ir.sequence'].next_by_code('move.pdfreports.ingresos', sequence_date=r.date) or _('')	
				#elif r.payment_type == 'outbound' and not r.is_internal_transfer :
				elif r.payment_type == 'outbound':
					r.extra_sequence=self.env['ir.sequence'].next_by_code('move.pdfreports.egresos', sequence_date=r.date) or _('')	
				else :
					r.extra_sequence=self.env['ir.sequence'].next_by_code('move.pdfreports.traspasos', sequence_date=r.date) or _('')
			elif r.state=='posted' and (not r.extra_sequence or r.extra_sequence=='') and not r.a :
				if r.payment_type == 'inbound' and not r.is_internal_transfer:
					r.extra_sequence=self.env['ir.sequence'].next_by_code('move.pdfreports.ingresos2', sequence_date=r.date) or _('')	
				#elif r.payment_type == 'outbound' and not r.is_internal_transfer :
				elif r.payment_type == 'outbound':
					r.extra_sequence=self.env['ir.sequence'].next_by_code('move.pdfreports.egresos2', sequence_date=r.date) or _('')	
				else :
					r.extra_sequence=self.env['ir.sequence'].next_by_code('move.pdfreports.traspasos2', sequence_date=r.date) or _('')

class AccountMoveLine(models.Model):
	#Hereda todo y modifica
	_inherit = 'account.move.line'
	
	#Crea los siguientes campos
	a = fields.Boolean(string='Centro de Costos :', store=True, readonly=False, compute='_move_id_a')
	extra_sequence = fields.Char(string='Secuencia Mensual', readonly=True, store=True, states={'draft': [('readonly', False)]}, compute='_extra_sequence_line')
	
	@api.depends('move_id.a')
	def _move_id_a(self): 
		for r in self:
			r.a = r.move_id.a
			
	@api.depends('move_id.extra_sequence')
	def _extra_sequence_line(self): 
		for r in self:
			r.extra_sequence = r.move_id.extra_sequence