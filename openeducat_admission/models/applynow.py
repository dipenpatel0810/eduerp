from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, UserError


class applynow(models.Model):
    _name = 'applynow'
    _inherits= {'res.users': 'user_id'}
    email_id=fields.Char('Email-ID',required=True)

    @api.multi
    def send_my_mail(self):
        self.user_id.action_reset_password()


    @api.model
    def create(self,values):
        group_id = self.env.ref('openeducat_admission.group_applicant')
        values['groups_id'] = [(4,group_id.id)]
        res = super(applynow,self).create(values)
        # for setting email id in Partner 
        res.user_id.partner_id.email = res.email_id 
        return res