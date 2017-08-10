from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, UserError

class OpAdmission(models.Model):
    _name = 'op.admission'
    _inherit = 'mail.thread'
    _rec_name = 'application_number'
    _order = "application_number desc"
    _description = "Admission"

    @api.model
    def _get_user(self):
        user = self.env['res.users'].search([('id','=',self.env.user.id)])
        # rec.stu_ids1 = student and student[0].id or False
        if user:
            return user[0].id

    user_default = fields.Many2one('res.users', string="User",default=_get_user)
    name = fields.Char(
        'First Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    middle_name = fields.Char(
        'Middle Name', size=128,
        states={'done': [('readonly', True)]})
    last_name = fields.Char(
        'Last Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    title = fields.Many2one(
       'res.partner.title', 'Title', states={'done': [('readonly', True)]})
    application_number = fields.Char(
        'Application Number', size=16, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self:
        self.env['ir.sequence'].next_by_code('op.admission'))
    admission_date = fields.Date(
        'Admission Date', copy=False,
        states={'done': [('readonly', True)]})
    application_date = fields.Datetime(
        'Application Date', required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self: fields.Datetime.now())
    birth_date = fields.Date(
        'Birth Date', required=True, states={'done': [('readonly', True)]})
    course_id = fields.Many2one(
        'op.course', 'Course', required=True,
        states={'done': [('readonly', True)]})
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True,
        states={'done': [('readonly', True)],
                'fees_paid': [('required', True)]})
    street = fields.Char(
        'Street', size=256, states={'done': [('readonly', True)]})
    street2 = fields.Char(
        'Street2', size=256, states={'done': [('readonly', True)]})
    phone = fields.Char(
        'Phone', size=16, states={'done': [('readonly', True)]})
    mobile = fields.Char(
        'Mobile', size=16, states={'done': [('readonly', True)]})
    # email = fields.Char(
    #     'Email', size=256, states={'done': [('readonly', True)]})
    city = fields.Char('City', size=64, states={'done': [('readonly', True)]})
    zip = fields.Char('Zip', size=8, states={'done': [('readonly', True)]})
    state_id = fields.Many2one(
        'res.country.state', 'States', states={'done': [('readonly', True)]})
    country_id = fields.Many2one(
        'res.country', 'Country', states={'done': [('readonly', True)]})
    fees = fields.Float('Fees', states={'done': [('readonly', True)]})
    photo = fields.Binary('Photo', states={'done': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('payment_process', 'Payment Process'), ('fees_paid', 'Fees Paid'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', readonly=True, select=True,
        default='draft', track_visibility='onchange')
    due_date = fields.Date('Due Date', states={'done': [('readonly', True)]})
    school_name = fields.Char('School Name',
        states={'done': [('readonly', True)]})
    school_namee = fields.Char('School Name',
        states={'done': [('readonly', True)]})
    hsc_result = fields.Char('HSC Result', states={'done': [('readonly', True)]})
    ssc_result = fields.Char(
        'SSC Result', size=256,states={'done': [('readonly', True)]} )
    prev_institute=fields.Char('Previous Institute',states={'done': [('readonly', True)]})
    prev_institute_course = fields.Many2one('op.course', 'Previous Course', states={'done': [('readonly', True)]})
    cgpa= fields.Char('CGPA/Grade')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')], 'Gender',
        required=True, states={'done': [('readonly', True)]})
    student_id = fields.Many2one(
        'op.student', 'Student', states={'done': [('readonly', True)]})
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register', required=True,
        states={'done': [('readonly', True)]})
    partner_id = fields.Many2one('res.partner', 'Partner')
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department', size=128, required=True)
    program_id = fields.Many2one('op.program', 'Program', required=True)
    program_type = fields.Many2one('op.program.type', string="Program Type",required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    # login = fields.Char(required=True,string='E-mail ID')
    caste = fields.Many2one('caste.category', string="Caste",required=True)
    sub_caste= fields.Many2one('subcaste.category', string="Sub-Caste")
    admtype = fields.Selection(
        [('1','SF'), ('2', 'NRI'), ('3','TFW'),('4','Government')],
        'Admission Type')
    nationality = fields.Many2one('res.country', 'Nationality')
    merit = fields.Integer('Merit Rank', required=True)
    contact = fields.Char(string="Contact Info")
    aadhar = fields.Char(string='Aadhar Card Number')
    religion = fields.Many2one('religion.category',string='Religion')
    minority= fields.Boolean(string ='Is Minority?')
    status=fields.Selection([('Single', 'Single'), ('Married', 'Married')],string='Status',required=True)
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    reg_no = fields.Char('Student ID',size=16,readonly=True,help="Auto Generate")
    applyy= fields.Boolean('For Applicant ID', default=True)
    rights= fields.Boolean('Rights', default=True)
    rights3 = fields.Boolean('Rights3',default=True)
    email_button = fields.Boolean('Email_Button',default=True)
    street1= fields.Char()
    street22 = fields.Char()
    city1 = fields.Char()
    state_id1= fields.Many2one('res.country.state')
    country_id1= fields.Many2one('res.country')
    zip1= fields.Char()
    phone1 = fields.Char()
    mobile1= fields.Char()

    @api.multi #for generating applicant id
    def generate_student_id(self, vals):
        
        bcode = self.env['op.batch'].search([('id','=',self.batch_id.id)]).code
        dcode = self.env['op.department'].search([('id','=',self.department_id.id)]).code
        cacode = self.env['caste.category'].search([('id','=',self.caste.id)]).code
    
        self.reg_no = bcode + dcode + cacode + self.env['ir.sequence'].next_by_code('op.admission') 
        self.applyy=False
        student = self.env['op.student'].search([('user_default','=',self.user_default.id)])
        student.reg_no = self.reg_no
        return super(OpAdmission, self)
        

    _defaults={
                      'reg_no': lambda obj, cr, uid, context: '/',
                        
               }

    # Accordig to the previous requirements. 
    # This would auto fill fields like Department, Program, Batch etc. based on the selection of "Admission Register"
    # @api.onchange('register_id')
    # def onchange_register(self):
    #     self.department_id = self.register_id.department_id
    #     self.program_id = self.register_id.program_id
    #     self.program_type = self.register_id.program_type
    #     self.campus_id = self.register_id.campus_id
    #     self.institute_id = self.register_id.institute_id
    #     self.batch_id = self.register_id.batch_id
    #     self.fees = self.register_id.product_id.lst_price

    @api.multi
    def admit_email(self):
        template = self.env.ref('openeducat_admission.admit_email')
        template.send_mail(self.user_default.partner_id.id, force_send=True)
        self.email_button=False

    @api.onchange('register_id')
    def onchange_register_id(self):
        self.fees = self.register_id.product_id.lst_price
        
    @api.onchange('batch_id','department_id','program_id','program_type',)
    def onchange_batch(self):
        self.register_id = self.env['op.admission.register'].search([('department_ids','=',self.department_id.id),('program_id','=',self.program_id.id),('batch_id','=',self.batch_id.id)])
        
    

    @api.one
    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        start_date = fields.Date.from_string(self.register_id.start_date)
        end_date = fields.Date.from_string(self.register_id.end_date)
        application_date = fields.Date.from_string(self.application_date)
        if application_date < start_date or application_date > end_date:
            raise ValidationError(_(
                "Application Date should be between Start Date & \
                End Date of Admission Register."))

    @api.one
    @api.constrains('birth_date')
    def _check_birthdate(self):
        if self.birth_date > fields.Date.today():
            raise ValidationError(_(
                "Birth Date can't be greater than current date!"))

    

    @api.multi
    def get_student_vals(self):
        return {
            'title': self.title and self.title.id or False,
            'name': self.name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'course_id': self.course_id and self.course_id.id or False,
            'batch_id': self.batch_id and self.batch_id.id or False,
            'campus_id' : self.campus_id and self.campus_id.id or False,
            'institute_id' : self.institute_id and self.institute_id.id or False,
            'program_id' : self.program_id and self.program_id.id or False,
            'department_id' : self.department_id and self.department_id.id or False,
            'program_type' : self.program_type and self.program_type.id or False,
            # 'login' : self.login,
            'user_default' : self.user_default and self.user_default.id or False,
            'register_id' : self.register_id and self.register_id.id or False,
            'caste': self.caste and self.caste.id or False,
            'sub_caste': self.sub_caste and self.sub_caste.id or False,
            'nationality' : self.nationality and self.nationality or False,
            'aadhar' : self.aadhar,
            'religion' : self.religion and self.religion.id or False,
            'minority' : self.minority,
            'status' : self.status,
            'merit' : self.merit,
            'photo': self.photo or False,
            'street': self.street or False,
            'street2': self.street2 or False,
            'phone': self.phone or False,
            'mobile': self.mobile or False,
            'zip': self.zip or False,
            'city': self.city or False,
            'country_id': self.country_id and self.country_id.id or False,
            'state_id': self.state_id and self.state_id.id or False,
            'reg_no': self.reg_no or False,
            'school_name': self.school_name or False,
            'school_namee': self.school_namee or False,
            'hsc_result': self.hsc_result or False,
            'ssc_result': self.ssc_result or False,
            'prev_institute': self.prev_institute or False,
            'prev_institute_course': self.prev_institute_course or False,
            'cgpa':self.cgpa or False,
            'parent_email' : self.parent_email,
            'user_parent' : self.user_parent and self.user_parent.id or False,
            'select': self.select or False,
            'aadharcardno': self.aadharcardno or False,
            'bankacnumber': self.bankacnumber or False,
            'pancardno': self.pancardno or False,
            'street1': self.street1 or False,
            'street22': self.street22 or False,
            'phone1': self.phone1 or False,
            'mobile1': self.mobile1 or False,
            'zip1': self.zip1 or False,
            'city1': self.city1 or False,
            'country_id1': self.country_id1 and self.country_id1.id or False,
            'state_id1': self.state_id and self.state_id1.id or False,
            'pstreet': self.street1 or False,
            'pstreet2': self.street22 or False,
            'pphone': self.phone1 or False,
            'pmobile': self.mobile1 or False,
            'pzip': self.zip1 or False,
            'pcity': self.city1 or False,
            'pcountry_id': self.country_id1 and self.country_id1.id or False,
            'pstate_id': self.state_id and self.state_id1.id or False,


        }

    @api.one
    def enroll_student(self):
        total_admission = self.env['op.admission'].search_count(
            [('register_id', '=', self.register_id.id),
             ('state', '=', 'done')])
        if self.register_id.max_count:
            if not total_admission < self.register_id.max_count:
                msg = 'Max Admission In Admission Register :- (%s)' % (
                    self.register_id.max_count)
                raise ValidationError(_(msg))

        vals = self.get_student_vals()
        vals.update({'partner_id': self.partner_id.id})
        self.write({
            'nbr': 1,
            'state': 'done',
            'admission_date': fields.Date.today(),
            'student_id': self.env['op.student'].create(vals).id,
        })
        self.student_id.get_subjects()
        self.student_id.onchange_batch_id()
        self.student_id.onchange_course_ids()

    @api.one
    def confirm_in_progress(self):
        self.state = 'confirm'
        if self.partner_id:
            self.state = 'payment_process'

    @api.one
    def confirm_rejected(self):
        self.state = 'reject'

    @api.one
    def confirm_pending(self):
        self.state = 'pending'

    @api.one
    def confirm_to_draft(self):
        self.state = 'draft'

    @api.one
    def confirm_cancel(self):
        self.state = 'cancel'

    @api.one
    def payment_process(self):
        self.state = 'fees_paid'

    @api.multi
    def open_student(self):
        form_view = self.env.ref('openeducat_core.view_op_student_form')
        tree_view = self.env.ref('openeducat_core.view_op_student_tree')
        # self.access_student() <- Used for giving access rights of group "Student" to the related user
        value = {
            'domain': str([('id', '=', self.student_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.student_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value

    # @api.multi
    # def rights_test(self):
    #     find_student = self.env['op.student'].search([('user_default','=',self.user_default.id)])
    #     print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",find_student
    #     find_student.partner_id.email = self.user_default.partner_id.email


    @api.multi
    def access_student(self):
        # self.partner_id.email = self.user_default.partner_id.email
        # student_id.partner_id.email = student_id.user_default.partner_id.email
        find_student = self.env['op.student'].search([('user_default','=',self.user_default.id)])
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",find_student
        find_student.partner_id.email = self.user_default.partner_id.email
        self.rights=False
        group_id = self.env.ref('openeducat_core.group_op_student')
        values = {'groups_id': [(4,group_id.id)]}
        res = self.user_default.write(values) 
        return res

    @api.multi
    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        inv_obj = self.env['account.invoice']
        partner_id = self.env['res.partner'].create({'name': self.name})

        account_id = False
        product = self.register_id.product_id
        if product.id:
            account_id = product.property_account_income_id.id
        if not account_id:
            account_id = product.categ_id.property_account_income_categ_id.id
        if not account_id:
            raise UserError(
                _('There is no income account defined for this product: "%s". \
                   You may have to install a chart of account from Accounting \
                   app, settings menu.') % (product.name,))

        if self.fees <= 0.00:
            raise UserError(_('The value of the deposit amount must be \
                             positive.'))
        else:
            amount = self.fees
            name = product.name

        invoice = inv_obj.create({
            'name': self.name,
            'origin': self.application_number,
            'type': 'out_invoice',
            'reference': False,
            'account_id': partner_id.property_account_receivable_id.id,
            'partner_id': self.user_default.partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'origin': self.application_number,
                'account_id': account_id,
                'price_unit': amount,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': self.register_id.product_id.uom_id.id,
                'product_id': product.id,
            })],
        })
        invoice.compute_taxes()

        form_view = self.env.ref('account.invoice_form')
        tree_view = self.env.ref('account.invoice_tree')
        value = {
            'domain': str([('id', '=', invoice.id)]),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': invoice.id,
            'target': 'current',
            'nodestroy': True
        }
        self.partner_id = partner_id
        self.state = 'payment_process'
        return value


