from openerp import models, fields, api
from openerp.exceptions import ValidationError, Warning


class OpParent(models.Model):
    _name = 'op.parent'
    _inherits= {'res.users': 'user_id'}

    @api.model
    def _get_defa_user(self):
        user = self.env['res.users'].search([('id','=',self.env.user.id)])
        if user:
            return user[0].id

    user_defa = fields.Many2one('res.users', string="Related Student" ,default=_get_defa_user,readonly=True)

    select=fields.Selection([('Father','Father'),('Mother','Mother'),('Guardian','Guardian')], string='Whom do you want to make a user of this portal?', required=True)
    # student_id=fields.Many2one('op.student','Stduent(s)')
    mfirst_name= fields.Char('First Name', size=256)
    mmiddle_name = fields.Char('Middle Name', size=256)
    mlast_name = fields.Char('Last Name', size=256)
    mage=fields.Char('Age')
    ffirst_name= fields.Char('First Name', size=256)
    fmiddle_name = fields.Char('Middle Name', size=256)
    flast_name = fields.Char('Last Name', size=256)
    fage=fields.Char('Age')
    gfirst_name= fields.Char('First Name', size=256)
    gmiddle_name = fields.Char('Middle Name', size=256)
    glast_name = fields.Char('Last Name', size=256)
    gage=fields.Char('Age')
    _business = fields.Char(
        'Father\'s Occupation' , size=32)
    _income = fields.Float(
        'Father\'s Income ')
    _business2 = fields.Char(
        'Guardian\'s Occupation' , size=32)
    _income2 = fields.Float(
        'Guardian\'s Income ')
    _business1= fields.Char('Mother\'s Occupation', size=32)
    _income1= fields.Float('Mother\'s Income', size=32)

    pstreet = fields.Char('Street', size=256)
    pstreet2 = fields.Char('Street2', size=256)
    pphone = fields.Char('Phone', size=16)
    pmobile = fields.Char('Mobile', size=16)
    pcity = fields.Char('City', size=64)
    pzip = fields.Char('Zip', size=8)
    pstate_id = fields.Many2one('res.country.state', string='States')
    pcountry_id = fields.Many2one('res.country', string='Country')

    aadharcardno = fields.Char()
    bankacnumber = fields.Char()
    pancardno = fields.Char()
    ffname= fields.Char()
    mfname=fields.Char()


    @api.onchange('select')
    def onchange_select(self):
        if self.select=='Guardian':
            self.parent1='Guardian'

    @api.model
    def create(self,values):
        group_id = self.env.ref('openeducat_parent.group_op_parent')
        values['groups_id'] = [(4,group_id.id)]
        res = super(OpParent,self).create(values)
        res.user_id.partner_id.login = res.login
        return res

    @api.multi
    def post_data(self):
        parent_id = self.env['op.admission'].search([('id', '=', self._context.get('active_id', None))])
        parent_id.write({'parent': False}) 
        return {'type': 'ir.actions.act_window_close'}


class OpStudent(models.Model):
    _inherit = 'op.student'
    parent_ids = fields.Many2one('op.parent', string='Parent')
    parent_email = fields.Char(string="Email ID", readonly=True)
    user_parent = fields.Many2one('res.users',string="Related Parent", readonly=True)
    select = fields.Char('Parent')
    aadharcardno = fields.Char()
    bankacnumber = fields.Char()
    pancardno = fields.Char()
    pstreet= fields.Char()
    pstreet2 = fields.Char()
    pcity = fields.Char()
    pzip= fields.Char()
    pphone = fields.Char()
    pmobile= fields.Char()
    pstate_id = fields.Many2one('res.country.state', string='States')
    pcountry_id = fields.Many2one('res.country', string='Country')


class OpAdmission(models.Model):

    _inherit = 'op.admission'
    parent=fields.Boolean('Create a new Parent', default=True, copy=False)
    parent_email = fields.Char(string="Email ID", states={'confirm': [('readonly', True)]}, readonly=True)
    user_parent = fields.Many2one('res.users',string="Related Parent User",states={'confirm': [('readonly', True)]}, readonly=True)
    select = fields.Char('Parent', states={'confirm': [('readonly', True)]}, readonly=True)
    aadharcardno = fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    bankacnumber = fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    pancardno = fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    pstreet= fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    pstreet2 = fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    pcity = fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    pstate_id = fields.Many2one('res.country.state', string='States',states={'confirm': [('readonly', True)]}, readonly=True)
    pcountry_id = fields.Many2one('res.country', string='Country', states={'confirm': [('readonly', True)]}, readonly=True)
    pzip= fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    pphone = fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)
    pmobile= fields.Char(states={'confirm': [('readonly', True)]}, readonly=True)


    @api.multi
    def parent_wizard(self):
        return {    
            'type': 'ir.actions.act_window',
            'res_model': 'op.parent',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('openeducat_parent.view_op_parent_form').id,
            'nodestroy': True,
            'target':'new',
            }
        

    @api.multi
    def confirm_in_progress(self):
        parentsearch = self.env['op.parent'].search([('user_defa','=',self.user_default.id)])
        if parentsearch:
            self.parent_email = parentsearch.login
            self.user_parent = parentsearch.user_id
            self.user_parent.partner_id.email = parentsearch.login
            self.select = parentsearch.select
            self.aadharcardno= parentsearch.aadharcardno
            self.bankacnumber = parentsearch.bankacnumber
            self.pancardno=parentsearch.pancardno
            self.pstreet=parentsearch.pstreet
            self.pstreet2=parentsearch.pstreet2
            self.pcity=parentsearch.pcity
            self.pstate_id=parentsearch.pstate_id
            self.pcountry_id=parentsearch.pcountry_id
            self.pzip=parentsearch.pzip
            self.pphone=parentsearch.pphone
            self.pmobie=parentsearch.pmobile
            self.user_parent.action_reset_password()

        if(self.parent==True):
            raise ValidationError("Enter Parent Details")
        super(OpAdmission, self).confirm_in_progress()

                
            
             
       

        


# class ResUsers(models.Model):
#     _inherit = "res.users"

#     parent_ids = fields.One2many('op.parent', 'user_id', 'Parents')
