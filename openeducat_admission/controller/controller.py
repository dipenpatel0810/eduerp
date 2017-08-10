from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, UserError
from openerp.addons.web import http

class Apply_Now_Form(http.Controller):
    @http.route('/applynow/applicationform', auth='public',website=True)
    def index(self, **kw):
    	# 1
        # return "Application Page coming soon!"
        # 2
        # return http.request.render('openeducat_admission.index', {
        #     'teachers': ["Winter", "is", "Coming"],
        # })
		# 3(ref)
		# Teachers = http.request.env['academy.teachers']
  #       return http.request.render('academy.index', {
  #           'teachers': Teachers.search([])
  #       })
        # 3(mine)++
        GOT = http.request.env['got']
        return http.request.render('openeducat_admission.index' , {
        	'westros' : GOT.search([])
        	})


# 3 (ref)
# class Teachers(models.Model):
#     _name = 'academy.teachers'
#     name = fields.Char()

# 3 (mine)
class GOT(models.Model):
	_name = 'got'
	name = fields.Char()
