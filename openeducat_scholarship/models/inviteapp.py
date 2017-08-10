from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class InviteApplicants(models.Model):
    _name = 'op.inviteapp'
    _inherit = 'mail.thread'
    scheme_id = fields.Many2one('op.scholarship.type', 'Scholarship Scheme', required=True)
    caste_ids = fields.Many2many(related = 'scheme_id.intended_for', string="Caste")
    campus_id = fields.Many2one(related = 'scheme_id.campus_id', string='Campus', size=128)
    institute_id = fields.Many2one(related = 'scheme_id.institute_id', string='Institute', size=128)
    department_ids = fields.Many2many(related = 'scheme_id.department_ids' , string='Department')
    program_ids = fields.Many2many(related = 'scheme_id.program_ids' , string='Program')
    student_ids = fields.Many2many('op.student' , string='Student/s')
    scho_type = fields.Many2one(related = 'scheme_id.scho_type', string='Scholarship Type')
    eval_type = fields.Many2many(related = 'scho_type.eval_type', string='Evaluation Criterias')
    sponsor = fields.Char(related = 'scheme_id.sponsor', string='Sponsor')
    req_att = fields.Selection(related = 'scheme_id.req_att', string='Attachments', readonly=True)
    sch_amount = fields.Float(related = 'scheme_id.sch_amount', string='Scholarship Amount')
    candidates = fields.Integer(related = 'scheme_id.candidates', string='Candidates Required')
    #sponsor details
    sponsor_name = fields.Char(related = 'scheme_id.sponsor_name', string='Name')
    sponsor_email_id = fields.Char(related = 'scheme_id.sponsor_email_id', string='Email Id')
    sponsor_contact_no = fields.Char(related = 'scheme_id.sponsor_contact_no',string='Contact number')
    sponsor_address = fields.Text(related = 'scheme_id.sponsor_address',string='Address Details')
    interval = fields.Selection(related = 'scheme_id.interval',string='Scholarship Period', readonly=True)
    start_date = fields.Date(related='scheme_id.start_date', string='Start Date')
    end_date = fields.Date(related='scheme_id.end_date', string='End Date')
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('reject', 'Rejected'),
         ('change', 'Change Req.'), ('accept', 'Accepted')], 'State',
        default='draft', track_visibility='onchange')
    #merit
    add_note = fields.Text(related='scheme_id.additional_note', string='Additional notes')
    percentage = fields.Float(related='scheme_id.percentage',string='Percentage')
    percentile = fields.Float(related='scheme_id.percentile',string = 'Percentile')
    #financial
    income = fields.Float(related = 'scheme_id.income', string='Family Income')
    #sport
    sport = fields.Char(string='Sport Name')
    #research
    research = fields.Text(related = 'scheme_id.research', string='Research Field/Area with description')
    #career
    career = fields.Many2many(related = 'scheme_id.career', string='Career Option(s)')
    career_desc = fields.Text(related = 'scheme_id.career_desc',string="Career Field with description")
    #college
    achieve = fields.Char(related='scheme_id.achi', string='Achievement Field with description')
    achievement = fields.Selection(related='scheme_id.achievement',string="Personal Achievements", readonly=True)
    bond = fields.Integer(related='scheme_id.bond',string='Bond(in months)')
    #student
    gender = fields.Selection(related='scheme_id.gender',string='Gender', readonly=True)
    religion = fields.Many2many(related='scheme_id.religion', string="Religion")
    brand_name = fields.Char(related='scheme_id.brand_name',string="Brand Name")
    brand_org = fields.Text(related='scheme_id.brand_org',string="Address Details")
    brand_no = fields.Integer(related='scheme_id.brand_no',string="Contact Number")
    brand_mail = fields.Char(related='scheme_id.brand_mail',string="Email Id")
    product = fields.Char(related='scheme_id.promoting',string="Product for promotion")
    prod_details = fields.Text(related='scheme_id.prod_details',string="Product Details")
    contest = fields.Char(related='scheme_id.contest',string="Contest Name")
    contest_details = fields.Text(related='scheme_id.contest_details',string="Contest Description")


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

    @api.onchange('scheme_id')
    def onchange_caste_id(self):
        self.sport=self.scheme_id.sport_name
        if self.sport=='Other':
            self.sport=self.scheme_id.other_sport
    @api.onchange('scheme_id','department_ids','program_ids','caste_ids')
    def get_students(self):
        student_search = self.env['op.student'].search([('caste','in',self.caste_ids.ids),('department_id','in',self.department_ids.ids),('program_id','in',self.program_ids.ids)])
        self.student_ids =[i.id for i in student_search]
    @api.multi
    def act_applynow(self):
        # self.state = 'applied'
        res = {'name' : 'AppForm',
                'view_type' : 'form',
                'view_mode' : 'form,tree',
                'res_model' : 'applicationform',
                'type' : 'ir.actions.act_window',
                
                }
        return res