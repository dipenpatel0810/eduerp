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

from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class TimeTableReport(models.TransientModel):
    _name = 'time.table.report'
    _description = 'Generate Time Table Report'

    state = fields.Selection(
        [('faculty', 'Faculty'), ('student', 'Student')],
        string='Select', required=True, default='faculty')
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department', size=128, )
    program_id = fields.Many2one('op.program', 'Program', )
    program_type = fields.Many2one('op.program.type', string="Program Type")
    batch_id = fields.Many2one('op.batch', 'Batch')
    section_id = fields.Many2one('op.section', string="Section")
    course_id = fields.Many2one('op.course', string="Course")
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    start_date = fields.Date(
        'Start Date', required=True,
        default=(datetime.today() - relativedelta(
            days=datetime.date(
                datetime.today()).weekday())).strftime('%Y-%m-%d'))
    end_date = fields.Date(
        'End Date', required=True,
        default=(datetime.today() + relativedelta(days=6 - datetime.date(
            datetime.today()).weekday())).strftime('%Y-%m-%d'))

    @api.onchange('campus_id','institute_id')
    def get_faculty(self):
        return {'domain':{'faculty_id':[('campus_id','=',self.campus_id.id),('institute_id','=',self.institute_id.id)]}}

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if end_date < start_date:
            raise ValidationError(_('End Date cannot be set before \
            Start Date.'))
        elif end_date > (start_date + timedelta(days=6)):
            raise ValidationError(_("Select date range for a week!"))

    @api.multi
    def gen_time_table_report(self):
        data = self.read(
            ['start_date', 'end_date', 'course_id', 'batch_id', 'state',
             'faculty_id', 'campus_id', 'institute_id', 'department_id', 'program_id', 'program_type', 'section_id'])[0]
        if data['state'] == 'student':
            time_table_ids = self.env['op.timetable'].search(
                [('course_id', '=', data['course_id'][0]),
                 ('batch_id', '=', data['batch_id'][0]),
                 ('campus_id', '=', data['campus_id'][0]),
                 ('institute_id', '=', data['institute_id'][0]),
                 ('department_id', '=', data['department_id'][0]),
                 ('program_id', '=', data['program_id'][0]),
                 ('program_type', '=', data['program_type'][0]),
                 ('section_id', '=', data['section_id'][0]),
                 ('start_datetime', '>', data['start_date'] + '%H:%M:%S'),
                 ('end_datetime', '<', data['end_date'] + '%H:%M:%S')],
                order='start_datetime asc')

            data.update({'time_table_ids': time_table_ids.ids})
            return self.env['report'].get_action(
                self, 'openeducat_timetable.report_timetable_student_generate',
                data=data)
        else:
            teacher_time_table_ids = self.env['op.timetable'].search(
                [('start_datetime', '>', data['start_date'] + '%H:%M:%S'),
                 ('end_datetime', '<', data['end_date'] + '%H:%M:%S'),
                 ('faculty_id', '=', data['faculty_id'][0]),
                 ('campus_id', '=', data['campus_id'][0]),
                 ('institute_id', '=', data['institute_id'][0])],
                order='start_datetime asc')

            data.update({'teacher_time_table_ids': teacher_time_table_ids.ids})
            return self.env['report'].get_action(
                self, 'openeducat_timetable.report_timetable_teacher_generate',
                data=data)
