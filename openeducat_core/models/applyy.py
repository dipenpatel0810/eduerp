from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class Apply(models.Model):
    _name='op.applyy'
    _inherit = 'mail.thread'
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', string="Student", readonly=True)
    login= fields.Boolean('Login ID', default=False)
    email= fields.Boolean('E-mail Address', default=False)
    first_name = fields.Boolean('First Name',default=False)
    middle_name= fields.Boolean('Middle Name', default=False)
    last_name = fields.Boolean('Last Name', default=False)
    state= fields.Selection([('draft', 'Draft'), ('submit', 'Submit'),('confirm', 'Confirmed'),
         ('reject', 'Rejected'), ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', readonly=True, select=True,
        default='draft', track_visibility='onchange')
    caste = fields.Boolean('Caste', default=False)
    sub_caste = fields.Boolean('Sub-Caste', default=False)
    religion= fields.Boolean('Religion', default=False) 
    birth_date = fields.Boolean(string ='Birth Date', default=False)

    status=fields.Boolean(string='Status',default=False)
    visa_info = fields.Boolean('Visa Info', size=64,default=False)

    prev_login=fields.Char('Current Login ID', states={'submit':[('readonly', True)]})
    new_login= fields.Char('New Login ID', states={'submit':[('readonly', True)]})

    prev_email=fields.Char('Current E-mail Address', states={'submit':[('readonly', True)]})
    new_email= fields.Char('New E-mail Address', states={'submit':[('readonly', True)]})

    #Temporary Address
    temp_address=fields.Boolean(string="Address" ,default=False)
    phonee= fields.Boolean(string="Phone",default=False)
    mobilee= fields.Boolean(string="Mobile",default=False)

    #Permanent Address
    per_address=fields.Boolean(string="Address" ,default=False)
    phone2 = fields.Boolean(string="Phone",default=False)
    mobile2= fields.Boolean(string="Mobile",default=False)

    #personal
    aadhar = fields.Boolean(string='Aadhar Card Number', default=False)
    prev_fn= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_fn= fields.Char('New Record',states={'submit':[('readonly', True)]})
    prev_mn= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_mn= fields.Char('New Record', states={'submit':[('readonly', True)]})
    prev_ln= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_ln= fields.Char('New Record', states={'submit':[('readonly', True)]})
    prev_caste= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_caste= fields.Many2one('caste.category', states={'submit':[('readonly', True)]})
    prev_sub= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_sub= fields.Many2one('subcaste.category', string='New Record', states={'submit':[('readonly', True)]})
    prev_re= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_re= fields.Many2one('religion.category', string ='New Record', states={'submit':[('readonly', True)]})
    prev_aadhar= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_aadhar= fields.Char('New Record', states={'submit':[('readonly', True)]})

    #Permanent Address
    prev_phone= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_phone= fields.Char('New Record', states={'submit':[('readonly', True)]})
    prev_mobile= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_mobile= fields.Char('New Record', states={'submit':[('readonly', True)]})
    prev_street1= fields.Char(states={'submit':[('readonly', True)]})
    new_street1= fields.Char(states={'submit':[('readonly', True)]})
    prev_street22= fields.Char(states={'submit':[('readonly', True)]})
    new_street22= fields.Char(states={'submit':[('readonly', True)]})
    prev_city1= fields.Char(states={'submit':[('readonly', True)]})
    new_city1= fields.Char(states={'submit':[('readonly', True)]})
    prev_state_id1= fields.Char(states={'submit':[('readonly', True)]})
    new_state_id1= fields.Many2one('res.country.state', states={'submit':[('readonly', True)]})
    prev_country_id1= fields.Char(states={'submit':[('readonly', True)]})
    new_country_id1= fields.Many2one('res.country', states={'submit':[('readonly', True)]})
    prev_zip1= fields.Char(states={'submit':[('readonly', True)]})
    new_zip1= fields.Char(states={'submit':[('readonly', True)]})



    #Temporary Address
    prev_phone1= fields.Char('Previous Record',states={'submit':[('readonly', True)]})
    new_phone1= fields.Char('New Record', states={'submit':[('readonly', True)]})
    prev_mobile1= fields.Char('Previous Record',states={'submit':[('readonly', True)]})
    new_mobile1= fields.Char('New Record', states={'submit':[('readonly', True)]})
    prev_street= fields.Char(states={'submit':[('readonly', True)]})
    new_street= fields.Char(states={'submit':[('readonly', True)]})
    prev_street2= fields.Char(states={'submit':[('readonly', True)]})
    new_street2= fields.Char(states={'submit':[('readonly', True)]})
    prev_city= fields.Char(states={'submit':[('readonly', True)]})
    new_city= fields.Char(states={'submit':[('readonly', True)]})
    prev_state_id= fields.Char(states={'submit':[('readonly', True)]})
    new_state_id= fields.Many2one('res.country.state', states={'submit':[('readonly', True)]})
    prev_country_id= fields.Char(states={'submit':[('readonly', True)]})
    new_country_id= fields.Many2one('res.country', states={'submit':[('readonly', True)]})
    prev_zip= fields.Char(states={'submit':[('readonly', True)]})
    new_zip= fields.Char(states={'submit':[('readonly', True)]})

    



    prev_status= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_status= fields.Selection([('Single', 'Single'), ('Married', 'Married')],string='New Record', states={'submit':[('readonly', True)]})
    prev_visa= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_visa= fields.Char('New Record', states={'submit':[('readonly', True)]})
    prev_bd= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    new_bd= fields.Date('New Record', states={'submit':[('readonly', True)]})

    #parent
    prev= fields.Boolean('Get Previous Records', default=False)
    select= fields.Char('Related Parent User', states={'submit':[('readonly', True)]})
    parent_name= fields.Char('Name', states={'submit':[('readonly', True)]})
    parent_email = fields.Char('Login ID', states={'submit':[('readonly', True)]})
    aadharcardno = fields.Char('Aadhar Card Number', states={'submit':[('readonly', True)]})
    bankacnumber = fields.Char('Bank Account Number', states={'submit':[('readonly', True)]})
    pancardno = fields.Char('Pan Card Number', states={'submit':[('readonly', True)]})

    #parent's contact
    con= fields.Boolean("Phone", default=False)
    con1 = fields.Boolean("Mobile", default=False)
    pprev_phone= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    pnew_phone= fields.Char('New Record', states={'submit':[('readonly', True)]})
    pprev_mobile= fields.Char('Previous Record', states={'submit':[('readonly', True)]})
    pnew_mobile= fields.Char('New Record', states={'submit':[('readonly', True)]})

    #parent's address
    add= fields.Boolean("Get Previous Records", default=False)
    pprev_street1= fields.Char(states={'submit':[('readonly', True)]})
    pnew_street1= fields.Char(states={'submit':[('readonly', True)]})
    pprev_street22= fields.Char(states={'submit':[('readonly', True)]})
    pnew_street22= fields.Char(states={'submit':[('readonly', True)]})
    pprev_city1= fields.Char(states={'submit':[('readonly', True)]})
    pnew_city1= fields.Char(states={'submit':[('readonly', True)]})
    pprev_state_id1= fields.Char(states={'submit':[('readonly', True)]})
    pnew_state_id1= fields.Many2one('res.country.state', states={'submit':[('readonly', True)]})
    pprev_country_id1= fields.Char(states={'submit':[('readonly', True)]})
    pnew_country_id1= fields.Many2one('res.country', states={'submit':[('readonly', True)]})
    pprev_zip1= fields.Char(states={'submit':[('readonly', True)]})
    pnew_zip1= fields.Char(states={'submit':[('readonly', True)]})


    
    new_select= fields.Selection([('Father','Father'),('Mother','Mother'),('Guardian','Guardian')], string='Related Parent User', states={'submit':[('readonly', True)]})
    new_parent_name= fields.Char('Parent Name', states={'submit':[('readonly', True)]})
    new_parent_email = fields.Char('New Login ID', states={'submit':[('readonly', True)]})
    new_aadharcardno = fields.Char(' New Aadhar Card Number', states={'submit':[('readonly', True)]})
    new_bankacnumber = fields.Char(' New Bank Account Number', states={'submit':[('readonly', True)]})
    new_pancardno = fields.Char('New Pan Card Number', states={'submit':[('readonly', True)]})

    @api.one
    def confirm_changes(self):
        self.state = 'confirm'
        # if self.partner_id:
        #     self.state = 'payment_process'

    @api.one
    def reject_changes(self):
        self.state = 'reject'

    @api.multi
    def submit_changes(self):
        self.state = 'submit'
        # body_html = '''<ul>
        #     <li>
        #         State:
        #         <span> Draft </span>
        #         <span class="fa fa-long-arrow-right"></span>
        #         <span> Submit </span>
        #     </li>
        #     <li>
        #         First Name:
        #         <span> {} </span>
        #         <span class="fa fa-long-arrow-right"></span>
        #         <span> {} </span>
        #     </li>
        # </ul>
        # '''.format(self.student_id.name, self.new_fn)
        # self.message_post(subtype='openeducat_core.mt_apply_for_st_change_submit')

    @api.one
    def reset_to_draft(self):
        self.state = 'draft'

    @api.one
    def cancel_changes(self):
        self.state = 'cancel'

    def add_follower(self, cr, uid, ids, context=None):
        self.message_subscribe_users(cr, uid, ids, user_ids=[1], context=context)

    def create(self, cr, uid, values, context=None):
        apply_id = super(Apply, self).create(cr, uid, values, context=context)
        self.add_follower(cr, uid, [apply_id], context=context)
        return apply_id

    @api.multi
    def done_changes(self):
        #personal
        if self.first_name == True:
            self.student_id.name = self.new_fn
            self.student_id.user_default.name= self.new_fn
        if self.middle_name == True:
            self.student_id.middle_name = self.new_mn
        if self.last_name == True:
            self.student_id.last_name = self.new_ln
        if self.login == True:
            self.student_id.user_default.login = self.new_login
        if self.email == True:
            self.student_id.user_default.partner_id.email = self.new_email
        if self.caste == True:
            self.student_id.caste = self.new_caste
        if self.sub_caste == True:
            self.student_id.sub_caste = self.new_sub
        if self.religion == True:
            self.student_id.religion = self.new_re
        if self.birth_date == True:
            self.student_id.birth_date = self.new_bd
        if self.status == True:
            self.student_id.status = self.new_status
        if self.visa_info == True:
            self.student_id.visa_info = self.new_visa
        if self.aadhar == True:
            self.student_id.aadhar = self.new_aadhar
        #temp address
        if self.temp_address == True:
            self.student_id.street = self.new_street
            self.student_id.street2 = self.new_street2
            self.student_id.city= self.new_city
            self.student_id.state_id = self.new_state_id
            self.student_id.country_id = self.new_country_id
            self.student_id.zip = self.new_zip
        if self.phonee== True:
            self.student_id.phone = self.new_phone1
        if self.mobilee == True:
            self.student_id.mobile= self.new_mobile1

        #permanent address
        if self.per_address == True:
            self.student_id.street1 = self.new_street1
            self.student_id.street22 = self.new_street22
            self.student_id.city1= self.new_city1
            self.student_id.state_id1 = self.new_state_id1
            self.student_id.country_id1 = self.new_country_id1
            self.student_id.zip1 = self.new_zip1
        if self.phone2== True:
            self.student_id.phone1 = self.new_phone
        if self.mobile2 == True:
            self.student_id.mobile1= self.new_mobile

        #parent details
        if self.prev==True:
            self.student_id.select= self.new_select
            self.student_id.user_parent= self.new_parent_name
            self.student_id.parent_email= self.new_parent_email
            self.student_id.aadharcardno= self.new_aadharcardno
            self.student_id.bankacnumber= self.new_bankacnumber
            self.student_id.pancardno= self.new_pancardno

        #parent's address
        if self.add== True:
            self.student_id.pstreet= self.pnew_street1
            self.student_id.pstreet2 = self.pnew_street22
            self.student_id.pcity= self.pnew_city1
            self.student_id.pstate_id = self.pnew_state_id1
            self.student_id.pcountry_id = self.pnew_country_id1
            self.student_id.pzip = self.pnew_zip1

        #parent's contact
        if self.con== True:
            self.student_id.pphone= self.pnew_phone
        if self.con1==True:
            self.student_id.pmobile= self.pnew_mobile

        self.state = 'done'
       



    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'submit':
            return 'openeducat_core.mt_apply_for_st_change_submit'
        if 'state' in init_values and self.state == 'confirm':
            return 'openeducat_core.mt_apply_for_st_change_confirm'
        if 'state' in init_values and self.state == 'done':
            return 'openeducat_core.mt_apply_for_st_change_done'
        if 'state' in init_values and self.state == 'cancel':
            return 'openeducat_core.mt_apply_for_st_change_cancel'      
        if 'state' in init_values and self.state == 'reject':
            return 'openeducat_core.mt_apply_for_st_change_reject'

        return super(Apply, self)._track_subtype(init_values)



    @api.one
    @api.constrains('new_bd')
    def _check_birthdate(self):
        if self.new_bd > fields.Date.today():
            raise ValidationError(_(
                "Birth Date can't be greater than current date!"))

    @api.onchange('add')
    def onchange_add(self):
        if(self.add==True):
            self.pprev_street1= self.env['op.student'].browse(self.env.context['active_id']).pstreet
            self.pprev_street22 = self.env['op.student'].browse(self.env.context['active_id']).pstreet2
            self.pprev_city1 = self.env['op.student'].browse(self.env.context['active_id']).pcity
            self.pprev_state_id1 = self.env['op.student'].browse(self.env.context['active_id']).pstate_id.name
            self.pprev_zip1 = self.env['op.student'].browse(self.env.context['active_id']).pzip
            self.pprev_country_id1 = self.env['op.student'].browse(self.env.context['active_id']).pcountry_id.name


    @api.onchange('prev')
    def onchange_parent(self):
        if (self.prev==True):
            self.select= self.env['op.student'].browse(self.env.context['active_id']).select
            self.parent_name = self.env['op.student'].browse(self.env.context['active_id']).user_parent.name
            self.parent_email = self.env['op.student'].browse(self.env.context['active_id']).parent_email
            self.aadharcardno = self.env['op.student'].browse(self.env.context['active_id']).aadharcardno
            self.bankacnumber= self.env['op.student'].browse(self.env.context['active_id']).bankacnumber
            self.pancardno= self.env['op.student'].browse(self.env.context['active_id']).pancardno


    @api.onchange('login')
    def onchange_login(self):
        if(self.login==True):
            self.prev_login = self.env['res.users'].search([('id','=',self.env.user.id)]).login

    @api.onchange('email')
    def onchange_email(self):
        if(self.email==True):
            self.prev_email = self.env['res.users'].search([('id','=',self.env.user.id)]).partner_id.email
            
    @api.onchange('con')
    def onchange_con(self):
        if(self.con==True):
            self.pprev_phone = self.env['op.student'].browse(self.env.context['active_id']).pphone

    @api.onchange('con1')
    def onchange_con1(self):
        if(self.con1==True):
            self.pprev_mobile = self.env['op.student'].browse(self.env.context['active_id']).pmobile
            
    @api.onchange('first_name')
    def first(self):
        if(self.first_name==True):
            self.prev_fn = self.env['op.student'].browse(self.env.context['active_id']).name

    @api.onchange('middle_name')
    def middle(self):
        if(self.middle_name==True):
            self.prev_mn = self.env['op.student'].browse(self.env.context['active_id']).middle_name

    @api.onchange('last_name')
    def last(self):
        if(self.last_name==True):
            self.prev_ln = self.env['op.student'].browse(self.env.context['active_id']).last_name

    @api.onchange('birth_date')
    def onchange_birth_date(self):
        if(self.birth_date==True):
            self.prev_bd = self.env['op.student'].browse(self.env.context['active_id']).birth_date

    @api.onchange('caste')
    def onchange_caste(self):
        if(self.caste==True):
            self.prev_caste = self.env['op.student'].browse(self.env.context['active_id']).caste.name

    @api.onchange('sub_caste')
    def onchange_sub_caste(self):
        if(self.sub_caste==True):
            self.prev_sub = self.env['op.student'].browse(self.env.context['active_id']).sub_caste.scname

    @api.onchange('per_address')
    def onchange_per_address(self):
        if(self.per_address==True):
            self.prev_street1= self.env['op.student'].browse(self.env.context['active_id']).street1
            self.prev_street22 = self.env['op.student'].browse(self.env.context['active_id']).street22
            self.prev_city1 = self.env['op.student'].browse(self.env.context['active_id']).city1
            self.prev_state_id1 = self.env['op.student'].browse(self.env.context['active_id']).state_id1.name
            self.prev_zip1 = self.env['op.student'].browse(self.env.context['active_id']).zip1
            self.prev_country_id1 = self.env['op.student'].browse(self.env.context['active_id']).country_id1.name

    @api.onchange('temp_address')
    def onchange_temp_address(self):
        if(self.temp_address==True):
            self.prev_street= self.env['op.student'].browse(self.env.context['active_id']).street
            self.prev_street2 = self.env['op.student'].browse(self.env.context['active_id']).street2
            self.prev_city = self.env['op.student'].browse(self.env.context['active_id']).city
            self.prev_state_id = self.env['op.student'].browse(self.env.context['active_id']).state_id.name
            self.prev_zip = self.env['op.student'].browse(self.env.context['active_id']).zip
            self.prev_country_id = self.env['op.student'].browse(self.env.context['active_id']).country_id.name
            


    @api.onchange('phone2')
    def onchange_phone2(self):
        if(self.phone2==True):
            self.prev_phone = self.env['op.student'].browse(self.env.context['active_id']).phone1

    @api.onchange('mobile2')
    def onchange_mobile2(self):
        if(self.mobile2==True):
            self.prev_mobile = self.env['op.student'].browse(self.env.context['active_id']).mobile1

    @api.onchange('phonee')
    def onchange_phonee(self):
        if(self.phonee==True):
            self.prev_phone1 = self.env['op.student'].browse(self.env.context['active_id']).phone

    @api.onchange('mobilee')
    def onchange_mobilee(self):
        if(self.mobilee==True):
            self.prev_mobile1 = self.env['op.student'].browse(self.env.context['active_id']).mobile


    @api.onchange('status')
    def onchange_status(self):
        if(self.status==True):
            self.prev_status = self.env['op.student'].browse(self.env.context['active_id']).status

    @api.onchange('visa_info')
    def onchange_visa_info(self):
        if(self.visa_info==True):
            self.prev_visa = self.env['op.student'].browse(self.env.context['active_id']).visa_info


    @api.onchange('religion')
    def onchange_religion(self):
        if(self.religion==True):
            self.prev_re = self.env['op.student'].browse(self.env.context['active_id']).religion.name

    @api.onchange('aadhar')
    def onchange_aadhar(self):
        if(self.aadhar==True):
            self.prev_aadhar = self.env['op.student'].browse(self.env.context['active_id']).aadhar

    @api.multi
    def post_data(self):
        mail_id = self.env['op.student'].search([('id', '=', self._context.get('active_id', None))])
        # parent_id.write({'parent': False}) 
        return {'type': 'ir.actions.act_window_close'}
   


class Student(models.Model):
    _inherit = 'op.student'
    apply_id = fields.One2many(
        'op.applyy', 'student_id', 'Change Application')
    @api.multi
    def apply_changes(self):
        form_view = self.env.ref('openeducat_core.view_op_applyy_form')
        # tree_view = self.env.ref('openeducat_core.view_op_student_tree')
        value = {
            'type': 'ir.actions.act_window',
            'res_model': 'op.applyy',
            'view_type': 'form',
            'view_mode': 'form',
            'domain': [('id', '=', self.id), ('student_id', '=', self.id)],
            'context': {'default_student_id': self.id, },
            'target': 'current',
        }
        return value