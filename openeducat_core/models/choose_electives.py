from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpSubjectRecords(models.TransientModel):
    _name = "op.subjectrecord.wizard"
    course_id = fields.Many2one('op.course')
    subject_id = fields.Many2one('op.subject')
    select = fields.Boolean('Select?', default=True)
    student_id = fields.Many2one('op.student')
    wiz_id = fields.Many2one('op.student.elective.wizard', string="Wizard Id")
    subject_type = fields.Selection(
        [('core', 'CORE'), ('elective', 'ELECTIVE')],
        'Subject Type', default="core", required=True)
    sub_line_id = fields.Many2one('op.subjectrecord', string="Subject Line")

class ChooseElectives(models.TransientModel):
    _name = 'op.student.elective.wizard'
    course_id = fields.Many2one(
        'op.course', 'Course',
        default=lambda self: self.env['op.student'].browse(
            self.env.context['active_id']).course_id.id or False,
        readonly=True)
    electives_allowed = fields.Integer("No. of electives allowed",readonly=True)
    student_id = fields.Many2one('op.student', 'Student', default=lambda self:self.env['op.student'].browse(self.env.context['active_id']).id)
    subjectrecord_ids = fields.One2many('op.subjectrecord.wizard', 'wiz_id', default=lambda self:self._get_default())
    
    # @api.model
    def _get_default(self):
        student_id = self.env['op.student'].browse(self.env.context['active_id'])
        records = []
        for sub in student_id.subjectrecord_ids:
            if sub.subject_type == 'elective':
                records.append((0, 0, {
                        'course_id': student_id.course_id.id,
                        'subject_id': sub.subject_id.id,
                        'select': sub.select,
                        'student_id': student_id.id,
                        'subject_type': sub.subject_type,
                        'sub_line_id': sub.id,
                    }))
        return records
    @api.multi
    def done(self):
        student_id = self.env['op.student'].browse(self.env.context['active_id'])
        cnt = 0
        for sub in self.subjectrecord_ids:
            sub.sub_line_id.select = sub.select
            if sub.sub_line_id.select == True:
                cnt = cnt + 1
        if cnt > self.course_id.electives_allowed:
            raise ValidationError(_("Electives limit exceeded"))
        subjectrecord_ids = self.env['op.subjectrecord'].search([('student_id','=',student_id.id)])
        for i in subjectrecord_ids:
            if i.select == False:
                i.student_id = False
        #student_id.remove_unselected()
        #student_id.subject_to_elect = False

    @api.onchange('course_id')
    def onchange_course(self):
        self.electives_allowed = self.course_id.electives_allowed