from openerp import models, fields, api

class OpDepartment(models.Model):
    _name = 'op.department'

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    campus_id = fields.Many2one('op.campus', string="Campus", size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    hod = fields.Many2one('res.partner', string="Head of Department")
    program_ids = fields.One2many('op.program', 'department_id', string="Programs")
    faculty_ids = fields.One2many('op.faculty', 'department_id', string="Faculty")
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_department', False):
            lst = []
            lst.append(self.env.context.get('institute_id'))
            institutes = self.env['op.institute'].browse(lst)        
            departments = self.env['op.department'].search([('institute_id', 'in', lst)])
            return departments.name_get()
        return super(OpDepartment, self).name_search(
            name, args, operator=operator, limit=limit)
    _sql_constraints = [
            ('id_unique',
             'UNIQUE(code)',
             "The department id must be unique"),
    ]


 