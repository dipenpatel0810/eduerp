from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class StudentApply(models.Model):
    _name = 'stuapply'
    


    #_inherit = 'mail.thread'

   # scheme_ids1 = fields.Many2many('op.scholarship.type', 'Scholarship Scheme', required=True)
    @api.model
    def _get_students(self):
        student = self.env['op.student'].sudo().search([('user_default','=', self.env.user.id)])
        # rec.stu_ids1 = student and student[0].id or False
        if student:
            return student[0].id

    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Applied')], 'State',
        default='draft', track_visibility='onchange')
    stu_ids1 = fields.Many2one('op.student', string="Student",default=_get_students)
    scheme_id1 = fields.Many2many('op.inviteapp', string='Scholarship Scheme')

    

    
    @api.one
    def get_scheme(self):
        self.scheme_id1 = self.stu_ids1.scho_id2

    @api.one
    def act_apply(self):
        #self.state = 'apply'
        self.get_scheme()