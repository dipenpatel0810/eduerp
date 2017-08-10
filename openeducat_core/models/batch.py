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


class OpBatch(models.Model):
    _name = 'op.batch'
#2016 batch,2017 batch etc
    code = fields.Char('Code', size=32, required=True)
    name = fields.Char('Name', size=32, required=True)
    start_date = fields.Date(
        'Start Date', required=True, default=fields.Date.today())
    end_date = fields.Date('End Date', required=True)
    campus_id = fields.Many2one('op.campus', string='Campus', size=128, required=True)
    institute_id = fields.Many2one('op.institute', string='Institute', size=128, required=True)
    #batches come under institutes!!!!
    program_ids = fields.Many2many('op.program')
    student_ids = fields.One2many('op.student', 'batch_id')
   # course_id = fields.One2many('op.course', 'Course', required=True)
    _sql_constraints = [
            ('id_unique',
             'UNIQUE(code)',
             "The batch id must be unique"),
    ]

    @api.one
    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date > end_date:
            raise ValidationError(_("End Date cannot be set before \
            Start Date."))
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_batch', False):
            lst = []
            lst.append(self.env.context.get('institute_id'))
            lst2 = []
            lst2.append(self.env.context.get('program_id'))
            batches = self.env['op.batch'].search([('institute_id','in',lst),('program_ids','in',lst2)])
            return batches.name_get()
        return super(OpBatch, self).name_search(
            name, args, operator=operator, limit=limit)

#course hierarchy IT>ITsem>ITsess batch1=IT batch2=ITsem batch3=ITsess in roll no form if course selected is ITsess
#it will iterate its parents and find all the batches for all the parent courses as well so the batch DDL will show batch 1 2 and 3