
from openerp import models, fields, api

class OpProgram(models.Model):
    _name = 'op.program'

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    duration = fields.Char('Duration', required=True)
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department', size=128, required=True)
    program_types = fields.Many2many('op.program.type', string='Program types')
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_program', False):
            lst = []
            lst.append(self.env.context.get('department_id'))       
            programs = self.env['op.program'].search([('department_id', 'in', lst)])
            return programs.name_get()
        return super(OpProgram, self).name_search(
            name, args, operator=operator, limit=limit)
    _sql_constraints = [
            ('id_unique',
             'UNIQUE(code)',
             "The program id must be unique"),
    ]