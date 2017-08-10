from openerp import models, fields, api
import datetime

class OpFacultyHolidays(models.Model):
    _name = 'op.faculty.holiday.wizard'
    faculty_id = fields.Many2one('op.faculty', string='Faculty', 
    	default=lambda self:self.env['op.faculty'].browse(self.env.context.get('faculty_id')) 
    	or False, readonly=True)
    date_from = fields.Datetime(string="Start Date", 
    	default=lambda self:self.env['hr.holidays'].browse(self.env.context.get('record_id')).date_from
    	or False, readonly=True)
    date_to = fields.Datetime(string="End Date", 
    	default=lambda self:self.env['hr.holidays'].browse(self.env.context.get('record_id')).date_to
    	or False, readonly=True)
    time_table_ids = fields.One2many(
        'op.timetable.wizard', 'wiz_id', 'Time Table Lines')
    time_table_ids_1 = fields.One2many(
        'op.timetable.wizard', 'wiz_id', 'Time Table Lines')
    time_table_ids_2 = fields.One2many(
        'op.timetable.wizard', 'wiz_id', 'Time Table Lines')
    time_table_ids_3 = fields.One2many(
        'op.timetable.wizard', 'wiz_id', 'Time Table Lines')
    time_table_ids_4 = fields.One2many(
        'op.timetable.wizard', 'wiz_id', 'Time Table Lines')
    time_table_ids_5 = fields.One2many(
        'op.timetable.wizard', 'wiz_id', 'Time Table Lines')
    time_table_ids_6 = fields.One2many(
        'op.timetable.wizard', 'wiz_id', 'Time Table Lines')
    
    @api.onchange('date_from', 'date_to')
    def _get_default(self):
        records = []
    	records1 = []
        records2 = []
        records3 = []
        records4 = []
        records5 = []
        records6 = []
        if self.date_from and self.date_to:
            self_date_from = datetime.datetime.strptime(str(self.date_from), '%Y-%m-%d %H:%M:%S')
            self_date_from = self_date_from.replace(hour=00, minute=00, second=00)
            self_date_to = datetime.datetime.strptime(str(self.date_to), '%Y-%m-%d %H:%M:%S')
            self_date_to = self_date_to.replace(hour=23, minute=59, second=59)
            time_table_ids = self.env['op.timetable'].search([('faculty_id','=',self.faculty_id.id),
                ('start_datetime','>=',str(self_date_from)),
                ('start_datetime','<=',str(self_date_to))])
            for t in time_table_ids:
                date = datetime.datetime.strptime(t.start_datetime, '%Y-%m-%d %H:%M:%S').date()
                records.append((0,0,{'timetable_id': t.id, 'date': date}))
                if t.type == 'Monday':
                    records1.append((0,0,{'timetable_id': t.id, 'date': date}))
                if t.type == 'Tuesday':
                    records2.append((0,0,{'timetable_id': t.id, 'date': date}))
                if t.type == 'Wednesday':
                    records3.append((0,0,{'timetable_id': t.id, 'date': date}))
                if t.type == 'Thursday':
                    records4.append((0,0,{'timetable_id': t.id, 'date': date}))
                if t.type == 'Friday':
                    records5.append((0,0,{'timetable_id': t.id, 'date': date}))
                if t.type == 'Saturday':
                    records6.append((0,0,{'timetable_id': t.id, 'date': date}))
            self.time_table_ids = records
            self.time_table_ids_1 = records1
            self.time_table_ids_2 = records2
            self.time_table_ids_3 = records3
            self.time_table_ids_4 = records4
            self.time_table_ids_5 = records5
            self.time_table_ids_6 = records6
    @api.one
    def done(self):
        student_ids = []
        faculty_ids = []
        for t in self.time_table_ids:
            if t.new_faculty_id:
                t.timetable_id.faculty_id = t.new_faculty_id
                faculty_id = self.env['op.faculty'].browse(t.new_faculty_id.id)
                if faculty_id not in faculty_ids:
                    faculty_ids.append(faculty_id)
            else:
                t.timetable_id.cancel = True
                t.timetable_id.cancel_string = 'CANCELLED'
            for student in t.timetable_id.student_ids:
                if student not in student_ids:
                    student_ids.append(student)
        template = self.env.ref('openeducat_leave.notify_email')
        #template.with_context({'time_table_ids': self.time_table_ids}).send_mail(self.faculty_id.partner_id.id, force_send=True)
        for student in student_ids:
            timetable_ids = []
            for t in self.time_table_ids:
                if student in t.timetable_id.student_ids:
                    timetable_ids.append(t)     
            template.with_context({'timetable_ids': timetable_ids}).send_mail(student.user_default.partner_id.id, force_send=True)
        for faculty in faculty_ids:
            timetable_ids = []
            for t in self.time_table_ids:
                if faculty == t.timetable_id.faculty_id:
                    timetable_ids.append(t)
            template.with_context({'timetable_ids': timetable_ids}).send_mail(faculty.partner_id.id, force_send=True)
        self.env['hr.holidays'].browse(self.env.context.get('record_id')).check = True

        
class OpFaculty(models.Model):
    _inherit = 'op.faculty'
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_faculty', False):
            lst = []
            lst.append(self.env.context.get('subject_id')) 
            lst2 = []
            lst2.append(self.env.context.get('faculty_id'))
            timetable_id = self.env['op.timetable'].browse(self.env.context.get('timetable_id'))
            faculty = self.env['op.faculty'].search([('subject_ids', 'in', lst),('id','!=',lst2)])
            for f in faculty:
                timetable_search = self.env['op.timetable'].search([('faculty_id','=',f.id)])
                self_st_date = datetime.datetime.strptime(timetable_id.start_datetime, '%Y-%m-%d %H:%M:%S').date()
                self_st_time = datetime.datetime.strptime(timetable_id.start_datetime, '%Y-%m-%d %H:%M:%S').time()
                self_en_time = datetime.datetime.strptime(timetable_id.end_datetime, '%Y-%m-%d %H:%M:%S').time()
                for timetable in timetable_search:
                    if timetable.id != timetable_id.id:
                        st_date = datetime.datetime.strptime(timetable.start_datetime, '%Y-%m-%d %H:%M:%S').date()
                        st_time = datetime.datetime.strptime(timetable.start_datetime, '%Y-%m-%d %H:%M:%S').time()
                        en_time = datetime.datetime.strptime(timetable.end_datetime, '%Y-%m-%d %H:%M:%S').time()
                        if st_date == self_st_date:
                            if (self_st_time >= st_time and self_st_time < en_time) or (self_en_time > st_time and self_en_time <= en_time):
                                faculty = faculty - f
            return faculty.name_get()
        return super(OpFaculty, self).name_search(
            name, args, operator=operator, limit=limit)
class OpTimetableWizard(models.Model):
    _name = 'op.timetable.wizard'
    wiz_id = fields.Many2one('op.faculty.holiday.wizard', 'Faculty holiday wizard')
    timetable_id = fields.Many2one('op.timetable', string="Timetable")
    type = fields.Selection(related = 'timetable_id.type', string="Days")
    period_id = fields.Many2one(related = 'timetable_id.period_id', string="Period")
    subject_id = fields.Many2one(related = 'timetable_id.subject_id', string="Subject")
    faculty_id = fields.Many2one(related = 'timetable_id.faculty_id', string="Faculty")
    section_id = fields.Many2one(related = 'timetable_id.section_id', string="Section")
    new_faculty_id = fields.Many2one('op.faculty', string="Replacement Faculty")
    classroom_id = fields.Many2one(related = 'timetable_id.classroom_id', string="Classroom")
    date = fields.Date(string="Date")
class hr_holidays(models.Model):
    _inherit = 'hr.holidays'
    faculty_id = fields.Many2one(related = 'employee_id.faculty_id', string="Faculty")
    check = fields.Boolean(default=False)
    @api.multi
    def reschedule_wizard(self):
        record_id = self.env.context.get('record_id')
        return {    
            'type': 'ir.actions.act_window',
            'res_model': 'op.faculty.holiday.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new',
            'nodestroy': True,
            'context':"{'faculty_id':faculty_id,'record_id':record_id}"
        }

week_number = {
    'Mon': 1,
    'Tue': 2,
    'Wed': 3,
    'Thu': 4,
    'Fri': 5,
    'Sat': 6,
    'Sun': 7,
}

    