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

{
    'name': 'OpenEduCat Scholarship',
    'version': '9.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'Openerp Education',
    "sequence": 3,
    'summary': 'Manage Scholarship',
    'complexity': "easy",
    'description': """
        This module adds the feature of scholarship in Openeducat
    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core'],
    'update_xml' : ['views/sch_app.xml',
                ],
    'data': [
        'views/applicationform.xml',
        'views/scholarship_type_view.xml',
        'views/inviteapp_view.xml',
        'views/stuapply.xml',
        'views/caste.xml',
        'report/report_scholarship_generate.xml',
        'report/report_menu.xml',
        'wizard/scholarship_report.xml',
        'security/ir.model.access.csv',
        'scholarship_menu.xml',
    ],
    'demo': [
        'demo/scholarship_type_demo.xml',
        'demo/scholarship_demo.xml',
    ],
    'images': [
        'static/description/openeducat_scholarship_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}