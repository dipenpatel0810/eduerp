from openerp import models, fields, api, _

class OpResultRecords(models.Model):
	_name = "op.resultrecord"
	#_rec_name = "course_id"
	course_id = fields.Many2one('op.course')
	student_id = fields.Many2one('op.student')
	
	@api.multi
	def open_wizard(self):
		return {	
			'type': 'ir.actions.act_window',
			'res_model': 'op.marksheet.line',
			'view_type': 'form',
			'view_mode': 'tree,form',
			'target': 'new',
			'domain': [('student_id','=',self.student_id.id),('course_id','=',self.course_id.id)],
			#'context': "{'group_by':'session_id'}" 

		}

		







