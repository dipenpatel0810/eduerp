from openerp import models, fields, api
class OpEvaluation(models.Model):
    _name = 'op.evaluation'
    name = fields.Char('Name')
    exam_type_id = fields.Many2one('op.exam.type', string="Exam Type")
    max_marks = fields.Float('Max. marks')
    pass_marks = fields.Float('Passing marks')
    weightage = fields.Float('Weightage')
