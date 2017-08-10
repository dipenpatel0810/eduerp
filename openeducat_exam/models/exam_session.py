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
from openerp.exceptions import ValidationError


class OpExamSession(models.Model):
    _name = 'op.exam.session'
    _description = 'Exam Session'

    name = fields.Char('Exam', size=256, required=True)
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    department_id = fields.Many2one('op.department', string='Department', size=128, required=True)
    program_id = fields.Many2one('op.program', 'Program', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    exam_code = fields.Char('Exam Code', size=32, required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    room_id = fields.Many2one('op.exam.room', 'Room', required=True)
    exam_ids = fields.One2many('op.exam', 'session_id', 'Exam(s)')
    program_type = fields.Many2one('op.program.type', string="Program Type", required=True)
    @api.constrains('start_date', 'end_date')
    def _check_date_time(self):
        if self.start_date > self.end_date:
            raise ValidationError(_(
                'End Date cannot be set before Start Date.'))

    #@api.onchange('course_id')
    #def onchange_course(self):
    #    self.batch_id = False
