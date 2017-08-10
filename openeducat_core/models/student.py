# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, UserError




class SubCaste(models.Model):
    _name = 'subcaste.category'
    _rec_name = 'scname'
    scname = fields.Char(string='Sub-Caste ')

class Religion(models.Model):
    _name = 'religion.category'
    _rec_name = 'name'
    name = fields.Char(string='Religion')

class OpStudent(models.Model):
    _name = 'op.student'
    
    # _inherits= {'res.users' : 'user_id'}
    _inherits = {'res.partner': 'partner_id'}

    #@api.one
    #@api.depends('roll_number_line', 'batch_id', 'course_id')
    #def _get_curr_roll_number(self):
        # TO_DO:: Improve the logic by adding sequence field in course.
    #    if self.roll_number_line:
    #        for roll_no in self.roll_number_line:
    #            if roll_no.course_id == self.course_id and \
    #                    roll_no.batch_id == self.batch_id:
    #                self.roll_number = roll_no.roll_number
    #    else:
    #        self.roll_number = 0

    user_default = fields.Many2one('res.users')
    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128, required=True)
    birth_date = fields.Date('Birth Date', required=True)
    student_id = fields.Many2one(
        'op.student', 'Student')

    caste = fields.Many2one('caste.category', string="Caste",required=True)
    sub_caste= fields.Many2one('subcaste.category', string="Sub-Caste")
    admtype = fields.Selection(
        [('1','SF'), ('2', 'NRI'), ('3','TFW'),('4','Government')],
        'Admission Type')
    merit = fields.Integer('Merit Rank', required=True)
    scho_id2 = fields.Many2many('op.inviteapp', string="Scholarship")
    # hostel_display = fields.Many2many('op.hostel.room',string="Hostel")

    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    photo = fields.Binary('Photo')
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department', size=128, required=True)
    program_id = fields.Many2one('op.program', 'Program', required=True)
    program_type = fields.Many2one('op.program.type', string="Program Type")
    batch_id = fields.Many2one('op.batch', 'Batch', required=True,)
    section_id = fields.Many2one('op.section', string="Section")
    course_id = fields.Many2one('op.course', string="Course")
    roll_number_line = fields.One2many(
        'op.roll.number', 'student_id', 'Roll Number')
    partner_id = fields.Many2one('res.partner',string='Partner', required=False)
    roll_number = fields.Char(
        'Current Roll Number', compute='_get_curr_roll_number',
        size=8, store=True)
    # gr_no = fields.Char("GR Number", size=20)
    course_ids = fields.Many2many('op.course', string="Courses")
    result_ids = fields.One2many('op.resultrecord', 'student_id', string='Result Records')
    subjectrecord_ids = fields.One2many('op.subjectrecord', 'student_id', string="Subject Records")
    subject_to_elect = fields.Boolean('Subjects need to be elected', default=True)
    phone = fields.Char(string="Phone")
    mobile=fields.Char(string="Mobile")
    aadhar = fields.Char(string='Aadhar Card Number')
    religion = fields.Many2one('religion.category',string='Religion')
    minority= fields.Boolean(string ='Is Minority?')
    status=fields.Selection([('Single', 'Single'), ('Married', 'Married')],string='Status', required=True)
    reg_no = fields.Char('Student ID',size=16,readonly=True)
    street1= fields.Char()
    street22 = fields.Char()
    city1 = fields.Char()
    state_id1= fields.Many2one('res.country.state')
    country_id1= fields.Many2one('res.country')
    zip1= fields.Char()
    phone1 = fields.Char()
    mobile1= fields.Char()
    school_namee = fields.Char('School Name')
    school_name = fields.Char('School Name')
    hsc_result = fields.Char('HSC Result')
    ssc_result = fields.Char(
        'SSC Result', size=256)
    prev_institute=fields.Char('Previous Institute')
    prev_institute_course = fields.Many2one('op.course', 'Previous Course')
    cgpa= fields.Char('CGPA/Grade')
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register')
    invoice_date = fields.Datetime('Invoice Date',default=lambda self: fields.Datetime.now())

    @api.multi
    def fee_payment(self):
        inv_obj = self.env['account.invoice']
        product = self.register_id.product_id
        print "================register_id=====================",self.register_id
        account_id = False
        if product.id:
            account_id = product.property_account_income_id.id
        if not account_id:
            account_id = product.categ_id.property_account_income_categ_id.id
        if not account_id:
            raise UserError(
                _('There is no income account defined for this product: "%s". \
                   You may have to install a chart of account from Accounting \
                   app, settings menu.') % (product.name,))
        invoice = inv_obj.create({
            'name': self.name,
            'type': 'out_invoice',
            'partner_id': self.user_default.partner_id.id,
            'date_invoice' : self.invoice_date,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'name': product.name,
                'account_id': account_id,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': self.register_id.product_id.uom_id.id,
                'price_unit': self.register_id.product_id.lst_price  
            })],
        })
        for i in invoice.invoice_line_ids:
            i._set_taxes()
        

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
        return value

    @api.onchange('course_ids')
    def onchange_course_ids(self):
        for course in self.course_ids:
            vals ={
                'student_id': self.env.context.get('student_id'),
                'course_id': course.id,
            }
            self.result_ids += self.env['op.resultrecord'].new(vals)

    @api.onchange('course_id')
    def get_subjects(self):
        subject_ids = [j.id for j in self.course_id.subject_ids]
        elective_ids = [j.id for j in self.course_id.elective_ids]
        for subject in subject_ids:
            vals ={
                'student_id': self.env.context.get('student_id'),
                'course_id': self.course_id.id,
                'subject_id': subject,
                'select': True,
                'subject_type': 'core',
            }
            self.subjectrecord_ids += self.env['op.subjectrecord'].new(vals)
        for elective in elective_ids:
            vals ={
                'student_id': self.env.context.get('student_id'),
                'course_id': self.course_id.id,
                'subject_id': elective,
                'select': False,
                'subject_type': 'elective',
            }
            self.subjectrecord_ids += self.env['op.subjectrecord'].new(vals)

    @api.onchange('batch_id','program_id','program_type')
    def onchange_batch_id(self):
        course_ids = self.course_ids.search([('batch_id', '=', self.batch_id.id),('program_id','=',self.program_id.id), ('program_type', '=', self.program_type.id)])
        self.course_ids = [(6, 0, [i.id for i in course_ids])]
    @api.onchange('subjectrecord_ids')
    def onchange_select(self):
        for record in self.subjectrecord_ids:
            if record.select == False and record.subject_type == 'core':
                raise ValidationError(_("Core subjects are compulsory!"))
    @api.one
    @api.constrains('birth_date')
    def _check_birthdate(self):
        if self.birth_date > fields.Date.today():
            raise ValidationError(_(
                "Birth Date can't be greater than current date!"))
    @api.multi
    def electives_wizard(self):
        return {    
            'type': 'ir.actions.act_window',
            'res_model': 'op.student.elective.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new',
            'nodestroy': True,
        }
    #@api.onchange('course_id')
    #def onchange_course(self):
    #    self.batch_id = False

    def remove_unselected(self):
        s_ids = [i.id for i in self.subjectrecord_ids if i.select == False]
        self.subjectrecord_ids = self.env['op.subjectrecord'].browse(list(set(self.subjectrecord_ids.ids) - set(s_ids)))

