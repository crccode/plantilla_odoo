#

from odoo import models, api, _, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    autorizacion = fields.Char(string = 'Autorización N°')
    llave = fields.Char(string = 'Llave')
    leyenda = fields.Char(string = 'Leyenda Ley 453')
    limiteemision = fields.Date(string='Fecha Limite de Emision', domain=[('type', '!=', 'bank')])
    actividad_economica_id= fields.Many2one('res.actividad', string='Actividad Económica',readonly=False, index=True, tracking=1, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",) 
    impresion = fields.Selection(selection=[('carta_sin_imagen', 'Carta sin imagen'), ('carta_con_imagen', 'Carta con imagen'), ('pos', 'POS pequeño')])
