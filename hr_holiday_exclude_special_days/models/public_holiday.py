# -*- coding: utf-8 -*-
# © 2016 Jérôme Guerriat
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from openerp import api, exceptions, fields, models, tools


class PublicHoliday(models.Model):
    _name = "hr.public_holiday"

    date = fields.Date("Public Holiday Date", required=True)
    company_id = fields.Many2one('res.company', string="Company", required=True)
    name = fields.Char(string="Holiday Name", required=True)

    @api.multi
    def create_leaves(self):
        self.ensure_one()
        HRHolidays = self.env['hr.holidays']
        holiday_status_id = self.env['hr.holidays.status'].search(
            [('is_public_holiday', '=', True)], limit=1)
        employee_ids = self.env['hr.employee'].search(
            [('company_id', '=', self.company_id.id)])
        date_from, date_to = self.compensate_user_tz(self.date)

        values = {'name': self.name,
                  'type': 'remove',
                  'holiday_type': 'employee',
                  'holiday_status_id': holiday_status_id.id,
                  'date_from': date_from,
                  'date_to': date_to,
                  'number_of_days_temp': 1,
                  'state': 'confirm',
                  'is_batch': True,
                  }

        if not holiday_status_id:
            raise exceptions.ValidationError(
                'No Leave Type has been configured as Public Holiday. Please '
                'go to Configuration > Leave Types and tick the box "Public '
                'Holiday" on the desired leave type.')

        context = {'mail_create_nosubscribe': True,
                   'mail_create_nolog': True,
                   'mail_notrack': True,
                   'tracking_disable': True}

        for employee in employee_ids:
            values['employee_id'] = employee.id
            try:
                leave = HRHolidays.sudo().with_context(context).create(values)
                leave.with_context(context).holidays_validate()
            except exceptions.ValidationError, e:
                raise exceptions.ValidationError(
                    'The leave entries could not be generated as the following '
                    'error occurred:\n\n%s: %s' % (
                    employee.name, e.name))

    @api.multi
    def remove_leaves(self):
        self.ensure_one()
        HRHolidays = self.env['hr.holidays']
        holiday_status_id = self.env['hr.holidays.status'].search(
            [('is_public_holiday', '=', True)])
        date_from, date_to = self.compensate_user_tz(self.date)
        employee_ids = self.env['hr.employee'].search(
            [('company_id', '=', self.company_id.id)])
        holiday_ids = self.env['hr.holidays'].search(
            [('holiday_status_id', '=', holiday_status_id.id),
             ('date_from', '>=', date_from),
             ('date_to', '<=', date_to),
             ('employee_id', 'in', employee_ids.ids)])

        if self.env.user.has_group('base.group_configuration') \
                or self.env.user.has_group('base.group_hr_manager'):
            for holiday in holiday_ids:
                holiday.sudo().state = 'draft'
                holiday.sudo().unlink()
        else:
            raise exceptions.ValidationError(
                'You do not have the rights to delete leave entries')

    def compensate_user_tz(self, date):
        """
        Take date and compensate for user timezone
        :param date:
        :return:
        """
        date_obj = datetime.strptime(date,
                                     tools.DEFAULT_SERVER_DATE_FORMAT)
        date_from = datetime.combine(date_obj, datetime.min.time())
        date_to = datetime.combine(date_obj, datetime.max.time())
        user_tz_offset = fields.Datetime.context_timestamp(
            self.sudo(self._uid), date_from).tzinfo._utcoffset
        date_from_tz_comp = date_from - user_tz_offset
        date_to_tz_comp = date_to - user_tz_offset
        date_from_tz_comp_str = date_from_tz_comp.strftime(
            tools.DEFAULT_SERVER_DATETIME_FORMAT)
        date_to_tz_comp_str = date_to_tz_comp.strftime(
            tools.DEFAULT_SERVER_DATETIME_FORMAT)

        return date_from_tz_comp_str, date_to_tz_comp_str

    _sql_constraints = [
        ('unique_date',
         'UNIQUE (date, company_id)',
         'You should only have one public holiday per company and date')
    ]


class HRHolidaysStatus(models.Model):
    _inherit = 'hr.holidays.status'

    is_public_holiday = fields.Boolean('Public Holiday', default=False)

    @api.multi
    @api.constrains('is_public_holiday')
    def check_unique_public_holiday(self):
        for holiday_status in self:
            if holiday_status.is_public_holiday \
                    and self.env['hr.holidays.status'].search(
                        [('is_public_holiday', '=', True),
                         ('id', '!=', holiday_status.id)]):
                raise exceptions.ValidationError(
                    'You can only have one leave type set as Public Holiday')
