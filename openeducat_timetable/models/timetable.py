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

                       
import datetime
from datetime import time
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import pytz
from pytz import timezone

class OpTimetable(models.Model):
    _name = 'op.timetable'
    _description = 'TimeTables'
    _rec_name = 'faculty_id'
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department', size=128, required=True)
    program_id = fields.Many2one('op.program', 'Program', required=True)
    program_type = fields.Many2one('op.program.type', string="Program Type", required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    section_id = fields.Many2one('op.section', string="Section", required=True)
    course_id = fields.Many2one('op.course', string="Course", required=True)
    period_id = fields.Many2one('op.period', 'Period', required=True)
    classroom_id = fields.Many2one('op.classroom', 'Classroom', required=True)
    start_datetime = fields.Datetime(
        'Start Time', required=True,
        default=lambda self: fields.Datetime.now())
    end_datetime = fields.Datetime('End Time', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    subject_ids = []
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    color = fields.Integer('Color Index')
    student_ids = fields.Many2many('op.student', string='Students')
    type = fields.Selection(
        [('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
         ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
         ('Friday', 'Friday'), ('Saturday', 'Saturday')], 'Days')
    cancel = fields.Boolean(default=False)
    cancel_string = fields.Char()
    @api.onchange('cancel')
    def onchange_cancel(self):
        if self.cancel == True:
            self.cancel_string = 'CANCELLED'
        else:  
            self.cancel_string = False
    @api.constrains('faculty_id')
    def check_faculty(self):
        timetable_search = self.env['op.timetable'].search([('faculty_id','=',self.faculty_id.id)])
        self_st_date = datetime.datetime.strptime(self.start_datetime, '%Y-%m-%d %H:%M:%S').date()
        self_st_time = datetime.datetime.strptime(self.start_datetime, '%Y-%m-%d %H:%M:%S').time()
        self_en_time = datetime.datetime.strptime(self.end_datetime, '%Y-%m-%d %H:%M:%S').time()
        for timetable in timetable_search:
            if timetable.id != self.id:
                st_date = datetime.datetime.strptime(timetable.start_datetime, '%Y-%m-%d %H:%M:%S').date()
                st_time = datetime.datetime.strptime(timetable.start_datetime, '%Y-%m-%d %H:%M:%S').time()
                en_time = datetime.datetime.strptime(timetable.end_datetime, '%Y-%m-%d %H:%M:%S').time()
                if st_date == self_st_date:
                    if (self_st_time >= st_time and self_st_time < en_time) or (self_en_time > st_time and self_en_time <= en_time):
                        raise ValidationError(_('Faculty has a different commitment at the same time.'))

        
    @api.constrains('subject_id','classroom_id')
    def get_students(self):
        timetable_search = self.env['op.timetable'].search([('classroom_id','=',self.classroom_id.id)])
        self_st_date = datetime.datetime.strptime(self.start_datetime, '%Y-%m-%d %H:%M:%S').date()
        self_st_time = datetime.datetime.strptime(self.start_datetime, '%Y-%m-%d %H:%M:%S').time()
        self_en_time = datetime.datetime.strptime(self.end_datetime, '%Y-%m-%d %H:%M:%S').time()
        for timetable in timetable_search:
            if timetable.id != self.id:
                st_date = datetime.datetime.strptime(timetable.start_datetime, '%Y-%m-%d %H:%M:%S').date()
                st_time = datetime.datetime.strptime(timetable.start_datetime, '%Y-%m-%d %H:%M:%S').time()
                en_time = datetime.datetime.strptime(timetable.end_datetime, '%Y-%m-%d %H:%M:%S').time()
                if st_date == self_st_date:
                    if (self_st_time >= st_time and self_st_time < en_time) or (self_en_time > st_time and self_en_time <= en_time):
                        raise ValidationError(_('Classroom is not free.'))
        student_search = self.env['op.student'].search([('course_id','=',self.course_id.id),('section_id','=',self.section_id.id)])
        for student in student_search:
                if self.subject_id not in [i.subject_id for i in student.subjectrecord_ids if i.select == True]:
                    student_search = list(set(student_search) - set(student))
        self.student_ids = [(6, 0, [i.id for i in student_search])]
        if len(student_search)>self.classroom_id.capacity:
            raise ValidationError(_('Classroom capacity not enough. Choose a different classroom'))
    @api.onchange('campus_id','institute_id')
    def get_domain(self):
        return {'domain':{'classroom_id':[('campus_id','=',self.campus_id.id),('institute_id','=',self.institute_id.id)]}}

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):    
        if self.start_datetime > self.end_datetime:
            raise ValidationError(_(
                'End Time cannot be set before Start Time.'))

    @api.onchange('course_id')
    def get_subjects(self):
        self.subject_ids = [i.id for i in self.course_id.subject_ids]
        self.subject_ids.extend([i.id for i in self.course_id.elective_ids])
        return {'domain':{'subject_id':[('id','in',self.subject_ids)]}}

    @api.onchange('subject_id','section_id','course_id')
    def get_faculty(self):
        record_ids = self.env['op.faculty.subject'].search([('subject_id','=',self.subject_id.id),('course_id','=',self.course_id.id),('section_id.id','=',self.section_id.id)])
        faculty_ids = [i.faculty_id.id for i in record_ids]
        return {'domain':{'faculty_id':[('id','in',faculty_ids)]}}

    @api.onchange('start_datetime')
    def onchange_start_date(self):
        start_datetime = datetime.datetime.strptime(
            self.start_datetime, "%Y-%m-%d %H:%M:%S")
        if start_datetime and start_datetime.weekday() == 0:
            self.type = 'Monday'
        elif start_datetime and start_datetime.weekday() == 1:
            self.type = 'Tuesday'
        elif start_datetime and start_datetime.weekday() == 2:
            self.type = 'Wednesday'
        elif start_datetime and start_datetime.weekday() == 3:
            self.type = 'Thursday'
        elif start_datetime and start_datetime.weekday() == 4:
            self.type = 'Friday'
        elif start_datetime and start_datetime.weekday() == 5:
            self.type = 'Saturday'
    @api.multi
    def name_get(self):
        res = []
        for value in self:
            res.append([value.id, "%s %s %s" % (value.period_id.name, value.course_id.name, value.batch_id.name)]) 
        return res
