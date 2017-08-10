from openerp import models, fields, api

class OpSubjectRecords(models.Model):
	_name = "op.subjectrecord"
	course_id = fields.Many2one('op.course')
	subject_id = fields.Many2one('op.subject')
	select = fields.Boolean('Select?', default=True)
	student_id = fields.Many2one('op.student')
	subject_type = fields.Selection(
        [('core', 'CORE'), ('elective', 'ELECTIVE')],
        'Subject Type', default="core", required=True)