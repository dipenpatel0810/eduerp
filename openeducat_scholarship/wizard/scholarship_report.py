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


class ScholarshipReport(models.TransientModel):
    _name = 'scholarship.report'
    _description = 'Generate Scholarship Application'

    student_id  = fields.Many2one('op.student','Student')
    scho_name = fields.Many2one('op.scholarship.type','Scholarship')
    """
    start_date = fields.Date(
        'Start Date', required=True,
        default=(datetime.today() - relativedelta(
            days=datetime.date(
                datetime.today()).weekday())).strftime('%Y-%m-%d'))
    end_date = fields.Date(
        'End Date', required=True,
        default=(datetime.today() + relativedelta(days=6 - datetime.date(
            datetime.today()).weekday())).strftime('%Y-%m-%d'))
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
    """

    @api.multi
    def print_report(self):
        return self.env['report'].get_action(self, 'openeducat_scholarship.report_scholarship_generate')




     