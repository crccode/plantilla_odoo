#

from odoo import models, api, _, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    
    a = fields.Boolean(string='Centro de Costos :', default=True, required=True)