
from openerp import models, fields, api

class OpInstitute(models.Model):
    _name = 'op.institute'

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    dean = fields.Many2one('res.partner', string="Dean")
    type = fields.Selection(
        [('unaided_private', 'Unaided - Private'), ('govt_aided', 'Government Aided'),
         ('govt', 'Government'), ('unimanaged_private', 'University Managed - Private'), ('unimanaged_govt', 'University Managed - Government'), ('deemed_private', 'Deemed University(Private)'), ('central', 'Central University'),
          ('private_aided', 'Private Aided'), ('deemed_govt', 'Deemed University (Government)')], required=True)
    contact_no = fields.Char('Contact No.', size=16)
    department_ids = fields.One2many('op.department', 'institute_id', string="Departments")

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_institute', False):
            lst = []
            lst.append(self.env.context.get('campus_id'))
            campuses = self.env['op.campus'].browse(lst)        
            institutes = self.env['op.institute'].search([('campus_id', 'in', lst)])
            return institutes.name_get()
        return super(OpInstitute, self).name_search(
            name, args, operator=operator, limit=limit)
    _sql_constraints = [
            ('id_unique',
             'UNIQUE(code)',
             "The institute id must be unique"),
    ]