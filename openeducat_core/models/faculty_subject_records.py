from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpFacultySubjectRecords(models.Model):
    _name = 'op.faculty.subject'
    subject_id = fields.Many2one('op.subject', string="Subject", default=lambda self: self.env.context.get('subject_id'))
    department_id =fields.Many2one('op.department')
    institute_id = fields.Many2one('op.institute')
    faculty_id = fields.Many2one('op.faculty', string="Faculty")
    program_id = fields.Many2one('op.program', string="Program")
    program_type = fields.Many2one('op.program.type', string="Program Type")
    status = fields.Selection([('active', 'Active'),('inactive', 'Inactive')])
    batch_id = fields.Many2one('op.batch', string ="Batch")
    course_id = fields.Many2one('op.course', string="Course")
    section_id = fields.Many2one('op.section', string="Section")
    @api.onchange('subject_id')
    def verify(self):
    	faculty_ids = [i.id for i in self.subject_id.faculty_ids]
    	self.department_id = self.subject_id.department_id
    	self.institute_id = self.subject_id.institute_id
        return {'domain':{'faculty_id':[('id','in',faculty_ids)],'program_id':[('institute_id','=',self.subject_id.institute_id.id)]}}
    @api.onchange('program_id','batch_id','program_type')
    def change_section(self):
    	tmp_ids = self.course_id.search([('batch_id', '=', self.batch_id.id),('program_id','=',self.program_id.id), ('program_type', '=', self.program_type.id)])
        course_ids = [i.id for i in tmp_ids if self.env.context.get('subject_id') in i.subject_ids.ids or self.env.context.get('subject_id') in i.elective_ids.ids]
    	return {'domain':{'course_id':[('id','in',course_ids)]}}