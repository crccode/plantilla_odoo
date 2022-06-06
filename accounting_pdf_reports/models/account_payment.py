# -*- coding: utf-8 -*-

from odoo import models, api, _, fields


class AccountPayment(models.Model):
	#Hereda todo y modifica
	_inherit = 'account.payment'
	
	#Crea los siguientes campos
	a = fields.Boolean(string='Centro de Costos :', store=True, readonly=False, compute='_payment_id_a_journal')

	@api.depends('journal_id')
	def _payment_id_a_journal(self): 
		for r in self:
			r.a = r.journal_id.a
