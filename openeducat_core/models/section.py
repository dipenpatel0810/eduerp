from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpSection(models.Model):
    _name = 'op.section'
    code = fields.Char('Code', size=32, required=True)
    name = fields.Char('Name', size=32, required=True)
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department')
    program_id = fields.Many2one('op.program', string='Program')
    program_type = fields.Many2one('op.program.type', string="Program Type")
    batch_id = fields.Many2one('op.batch', string='Batch')
    student_ids = fields.One2many('op.student', 'section_id')
    faculty_subject_ids = fields.One2many('op.faculty.subject', 'section_id', string="Faculty subject records")
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_section', False):
            lst = []
            lst.append(self.env.context.get('batch_id'))
            batches = self.env['op.batch'].browse(lst)
            lst2 = []
            lst2.append(self.env.context.get('program_id'))
            programs = self.env['op.program'].browse(lst2)
            sections = self.env['op.section'].search([('batch_id', 'in', lst),('program_id','in',lst2)])
            return sections.name_get()
        return super(OpSection, self).name_search(
            name, args, operator=operator, limit=limit)
    _sql_constraints = [
            ('id_unique',
             'UNIQUE(code)',
             "The section id must be unique"),
    ]