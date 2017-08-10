from openerp import models, fields, api


class OpAllAttendeesWizard(models.TransientModel):
    _name = 'op.exam.getattendees'

    course_id = fields.Many2one(
        'op.course', 'Course',
        default=lambda self: self.env['op.exam'].browse(
            self.env.context['active_id']).session_id.course_id.id or False,
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch',
        default=lambda self: self.env['op.exam'].browse(
            self.env.context['active_id']).session_id.batch_id.id or False,
        readonly=True)
    program_id = fields.Many2one(
        'op.program', 'Program',
        default=lambda self: self.env['op.exam'].browse(
            self.env.context['active_id']).session_id.program_id.id or False,
        readonly=True)
    subject_id = fields.Many2one(
        'op.subject', 'Subject',
        default=lambda self: self.env['op.exam'].browse(
            self.env.context['active_id']).subject_id.id or False,
        readonly=True)


    student_ids = fields.Many2many('op.student', string='Add Student(s)')



    @api.one
    def confirm_student(self):
        for exam in self.env.context.get('active_ids', []):
            exam_browse = self.env['op.exam'].browse(exam)
            absent_list = [
                x.student_id for x in exam_browse.attendees_line]
            all_student_search = self.env['op.student'].search(
                [('course_id', '=', exam_browse.session_id.course_id.id),
                 ('batch_id', '=', exam_browse.session_id.batch_id.id)])
            for student in all_student_search:
                if exam_browse.subject_id not in [i.subject_id for i in student.subjectrecord_ids if i.select == True]:
                    all_student_search = list(set(all_student_search) - set(student))
            all_student_search = list(
                set(all_student_search) - set(absent_list))
            for student_data in all_student_search:
                vals = {'student_id': student_data.id, 'status': 'present',
                        'exam_id': exam}
                if student_data.id in self.student_ids.ids:
                    vals.update({'status': 'absent'})
                self.env['op.exam.attendees'].create(vals)
        
