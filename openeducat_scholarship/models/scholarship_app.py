from openerp import models, fields, api, osv

class OpScholarshipApp(models.Model):
    _name = 'op.scholarship.app'
    _inherit = 'mail.thread'
    _description = 'Scholarship Application'

    reg_no = fields.Char('Application ID',size=7,readonly=True,help="Auto Generate")
    
    #
    #_sql_constraints = [
      #  ('uniq_name', 'unique(reg_no)', 'This Reg.No is number already registered!') 
      #  ]


    #def create(self, cr, uid, vals, context=None):
        #sequence=self.pool.get('ir.sequence').get(cr, uid, 'reg_code')

        #vals['reg_no']=sequence
    #return super(OpScholarshipApp, self).create(cr, uid, vals, context=context)
    @api.model
    def create(self, vals):
        vals['reg_no'] = self.env['ir.sequence'].next_by_code('op.scholarship.app')
        #print ">>>>>>>>>>>>>>>>>>>>>>>", vals
        return super(OpScholarshipApp, self).create(vals)

    _defaults={
                'reg_no': lambda obj, cr, uid, context: '/',
                        
               }