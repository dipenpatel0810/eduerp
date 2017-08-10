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
#from openerp import models, pooler
#from openerp.report import report_sxw

# class ReportScholarship(report_sxw.rml_parse):
#     def __init__(self, cr, uid, name, context=None):
#         super(ReportScholarship, self).__init__(
#             cr, uid, name, context=context)
#         self.localcontext.update({
#             'time': time,
#             'get_object': self.get_object,
#             'get_full_name': self.get_full_name,
#         })

#     def get_full_name(self, data):
#         student_name = self.pool.get('op.student').browse(
#             self.cr, self.uid, data['student_id'][0])
#         return ' '.join([student_name.name,
#                          student_name.middle_name,
#                          student_name.last_name])






# class ReportScholarshipGenerate(models.AbstractModel):
#     _name = 'report.openeducat_scholarship.report_scholarship_generate'
#     _inherit = 'report.abstract_report'
#     _template = 'openeducat_scholarship.report_scholarship_generate'
#     _wrapped_report_class = ReportScholarship
