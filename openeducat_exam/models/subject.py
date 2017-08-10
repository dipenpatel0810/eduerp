
from openerp import models, fields


class OpSubject(models.Model):
    _inherit = 'op.subject'

    evaluation_ids = fields.Many2many('op.evaluation', string="Evaluation Methods")