from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class ApplicationForm(models.Model):
    _name = 'applicationform'

    @api.model
    def _get_students(self):
        student = self.env['op.student'].search([('user_default','=',self.env.user.id)])
        # rec.stu_ids1 = student and student[0].id or False
        if student:
            return student[0].id


    name_default = fields.Many2one('op.student', string="Name",default=_get_students)
    percentage = fields.Char(string="Enter your percentage")

    scheme1 = fields.Many2one('op.scholarship.type', 'Scholarship Scheme', required=True)
    scho_type= fields.Many2one('op.scholarshiptype','Scholarship Type')
    needed_documents = fields.Text(string="Required Documents")
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('reject', 'Rejected'),
         ('change', 'Change Req.'), ('accept', 'Accepted')], 'State',
        default='draft', track_visibility='onchange')
    
    @api.onchange('scheme1')
    def onchange_scheme(self):
        self.scho_type = self.scheme1.scho_type
        self.needed_documents = self.scheme1.needed_documents

    @api.one
    def act_draft(self):
        self.state = 'draft'
    
    @api.one
    def act_submit(self):
        self.state = 'submit'

    @api.one
    def act_accept(self):
        self.state = 'accept'

    @api.one
    def act_change_req(self):
        self.state = 'change'

    @api.one
    def act_reject(self):
        self.state = 'reject'