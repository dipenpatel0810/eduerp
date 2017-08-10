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
from openerp.exceptions import ValidationError, Warning






class CareerCategory(models.Model):
    _name= 'career.category'
    name = fields.Char('Career Type')


class OpScholarshipType(models.Model):
    _name = 'op.scholarship.type'

    name = fields.Char('Name',required=True)
    scheme_id = fields.Char('Scheme ID', readonly=True, help="Auto Generate")
     
    department_ids = fields.Many2many(
        'op.department' , string='Department', required = True)
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    program_ids = fields.Many2many('op.program', string='Program', required=True)
    scho_type= fields.Many2one('op.scholarshiptype','Scholarship Type',required=True)
    scho_percentage_req = fields.Boolean(related='scho_type.percentage_req', string='Percentage Required')
    scho_income_req = fields.Boolean(related='scho_type.income_req', string='Family Income Required')
    scho_sport_req = fields.Boolean(related='scho_type.sport_req', string='Sports Category')
    scho_caste_req = fields.Boolean(related='scho_type.caste_req', string='Caste(s) Required')
    scho_research_req = fields.Boolean(related='scho_type.research_req')
    scho_gender_req = fields.Boolean(related='scho_type.gender_req')
    scho_religion_req = fields.Boolean(related='scho_type.religion_req')
    #scho_medical_req = fields.Boolean(related='scho_type.medical_req')
    scho_career_req = fields.Boolean(related='scho_type.career_req')
    scho_achi_req = fields.Boolean(related='scho_type.achi_req')
    scho_bond_req = fields.Boolean(related='scho_type.bond_req')
    scho_brand_req = fields.Boolean(related='scho_type.brand_req')
    scho_contest_req = fields.Boolean(related='scho_type.contest_req')
    scho_college_req= fields.Boolean(related='scho_type.college_req')
    batch_id = fields.Many2many('op.batch', string='Batch', required=True)
    course_id = fields.Many2one('op.course', 'Course') 
    intended_for = fields.Many2many('caste.category', string= "Caste")
    sponsor = fields.Char(string='Sponsor', required=True)
    amount = fields.Float(string='Alloted Amount', required=True)
    additional_note = fields.Text('Additional notes')
    percentage=fields.Float(string='Percentage')
    percentile = fields.Float(string = 'Percentile')
    income = fields.Float(string='Family Income')
    #scho_no= fields.Many2one('op.scholarshiptype')
    gender= fields.Selection([('Male',"Male"),('Female',"Female"),('Both',"Both"),('Other',"Other")])
    religion= fields.Many2many('religion.category', string="Religion")
    career= fields.Many2many('career.category', string='Career Option(s)')
    career_desc = fields.Text(string="Career Field with description")
    achi= fields.Char('Achievement Field')
    achievement= fields.Selection([('Yes',"If yes, specify"),('No',"No")], string="Personal Achievements(if any)")
    bond= fields.Integer('Bond(in months)')
    sport_name = fields.Selection(
        [('BasketBall','BasketBall'), ('FootBall', 'FootBall'), ('Badminton','Badminton'),('Chess','Chess'),('Other', 'Other')],
        string='Sport Name')
    other_sport = fields.Char(string='Specify if other(s)')
    research = fields.Text(string='Research Field/Area with description')
    candidates= fields.Integer(string="Number of Candidates", required=True)
    brand_name = fields.Char(string="Brand Name")
    brand_org= fields.Text(string="Address Details")
    brand_no = fields.Integer(string="Contact Number")
    brand_mail= fields.Char(string="Email Id")
    promoting = fields.Char(string="Product for promotion")
    prod_details= fields.Text(string="Product Details")
    contest = fields.Char(string="Contest Name")
    contest_details= fields.Text(string="Contest Description")
    needed_documents = fields.Text(string="Required Documents")
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    interval = fields.Selection(
        [('Monthly','Monthly'), ('Annual', 'Annual'), ('Semester','Semester')],
        string='Interval')
    sch_amount = fields.Float(string='Scholarship Amount', required=True) 
    req_att = fields.Selection(
        [('Yes','Yes'), ('No', 'No')],
        string='Attachments(if any)')
    
    
    #sponsor details
    org_name = fields.Selection([('Organization','Organization'),('Institution','Institution'),('University','University'),('Co','College')],string='Sponser Type')
    sponsor_name=fields.Char('Name')
    sponsor_email_id = fields.Char(string='Email Id')
    sponsor_contact_no = fields.Char(string='Contact number')
    sponsor_address= fields.Text(string='Address Details')



    @api.constrains('amount')
    def check_amount(self):
        if self.amount <= 0:
            raise ValidationError(_('Enter proper Amount'))
    @api.onchange('department_ids')
    def onchange_program_id(self):
        l=[]
        for rec in self:
            for d in rec.department_ids:
                l += d.program_ids.ids 
            rec.program_ids = l    


    @api.model
    def create(self, vals):
        vals['scheme_id'] = self.env['ir.sequence'].next_by_code('op.scholarship.type')
        #print ">>>>>>>>>>>>>>>>>>>>>>>", vals
        return super(OpScholarshipType, self).create(vals)

    _defaults={
                'scheme_id': lambda obj, cr, uid, context: '/',
                        
               }
class ScholarshipType(models.Model):
    _name='op.scholarshiptype'
    name= fields.Char('Scholarship Type', required=True)
    eval_type= fields.Many2many('op.evalcrit.type', string="Evaluation Criteria")
    #scho_no_id = fields.Integer('Scholarship Type ID', required= True)
    sch_no_id = fields.Many2one('op.scholarship.type')
    percentage_req = fields.Boolean('Academic Records')
    income_req = fields.Boolean('Family Income')
    sport_req = fields.Boolean('Sports Specific')
    caste_req =fields.Boolean('Caste(s) Specific')
    research_req = fields.Boolean('Research Specific')
    gender_req = fields.Boolean('Gender Specific')
    religion_req = fields.Boolean('Religion Specific')
    #medical_req = fields.Boolean('Medical History(if any)')
    career_req = fields.Boolean('Field/Career Specific')
    college_req= fields.Boolean('College Specific')
    bond_req= fields.Boolean('Bond Specific')
    achi_req= fields.Boolean('Achievement Specific')
    brand_req = fields.Boolean('Brand Specific')
    contest_req=fields.Boolean('Contest Specific')
class EvalCrit(models.Model):
    _name='op.evalcrit.type'
    name = fields.Char('Criteria Name', required=True)
