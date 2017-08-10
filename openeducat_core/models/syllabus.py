from openerp import models, fields, api
class OpSyllabus(models.Model):
    _name = 'op.syllabus'
    subject_id = fields.Many2one('op.subject', 'Subject', default=lambda self: self.env.context.get('subject_id'))
    data = fields.Binary('File')
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    status = fields.Selection([('active', 'Active'),('inactive', 'Inactive')])