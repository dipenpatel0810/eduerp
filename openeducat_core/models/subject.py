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
import base64
from tempfile import TemporaryFile
class OpSubject(models.Model):
    _name = 'op.subject'

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    campus_id = fields.Many2one('op.campus', 'Campus')
    institute_id = fields.Many2one('op.institute', 'Institute')
    department_id = fields.Many2one('op.department', 'Department')
    credits = fields.Float('Credits')
    type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Type', default="theory", required=True)
    faculty_ids = fields.Many2many('op.faculty')
    faculty_subject_ids = fields.One2many('op.faculty.subject', 'subject_id', string="Faculty subject records")
    student_id = fields.Many2one('op.student')
    course1_ids = fields.Many2many('op.course', 'course_subject_rel', 'subject_id', 'course_id')
    course2_ids = fields.Many2many('op.course', 'course_elective_rel', 'elective_id', 'course_id')
    syllabus_ids = fields.One2many('op.syllabus', 'subject_id', string="Syllabus")
    
    lecture_hours = fields.Integer(string="Theory hours per week")
    lab_hours = fields.Integer(string="Lab hours per week")
    note = fields.Text(string="Description")
    _sql_constraints = [
            ('id_unique',
             'UNIQUE(code)',
             "The subject id must be unique"),
    ]