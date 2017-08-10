# -*- coding: utf-8 -*-
{
    'name': "Leave Management",

    'summary': 'Extending hr leave management to add functionality of rescheduling lectures',

    'description': 'This module provides feature of leave management for faculty members',

    'author': "DDU",
    'website': "http://edu.inodoo.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['openeducat_timetable','hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/faculty_holidays_view.xml',
        'views/email_template.xml',

       # 'menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}