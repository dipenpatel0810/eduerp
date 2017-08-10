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

from openerp import models, fields, api


class OpCourse(models.Model):
    _name = 'op.course'

    name = fields.Char('Name', size=32, required=True)
    code = fields.Char('Code', size=8, required=True)
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department', size=128, required=True)
    program_id = fields.Many2one('op.program', string='Program', size=128, required=True)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Evaluation Type', default="normal", required=True)
    start_date = fields.Date(
        'Start Date', required=True, default=fields.Date.today())
    end_date = fields.Date('End Date', required=True)
    batch_id = fields.Many2one('op.batch', string="Batch")
    electives_allowed = fields.Integer(string="No. of electives allowed")
    subject_ids = fields.Many2many('op.subject', 'course_subject_rel', 'course_id', 'subject_id', string='Subject(s)')
    elective_ids = fields.Many2many('op.subject', 'course_elective_rel', 'course_id', 'elective_id', string='Elective(s)')
    program_type = fields.Many2one('op.program.type', string="Program Type", required=True)
    state = fields.Selection([
        ('draft', "Draft"),
        ('active', "Active"),
        ('inactive', "Inactive"),
    ])
    today = fields.Date.today()
    sequence = fields.Integer('Sequence')
    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_active(self):
        self.state = 'active'

    @api.multi
    def action_inactive(self):
        self.state = 'inactive'

   # _sql_constraints = [
    #        ('id_unique',
    #         'UNIQUE(code)',
    #         "The course id must be unique"),
    #]
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_course', False):
            lst = []
            lst.append(self.env.context.get('program_id')) 
            lst2 = []
            lst2.append(self.env.context.get('batch_id'))
            lst3 = []
            lst3.append(self.env.context.get('program_type'))
            courses = self.env['op.course'].search([('program_id', '=', lst),('batch_id','=',lst2),('program_type','=',lst3)])
            return courses.name_get()
        return super(OpCourse, self).name_search(
            name, args, operator=operator, limit=limit)