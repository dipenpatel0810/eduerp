from openerp import models, fields, api

class OpProgramType(models.Model):
    _name = 'op.program.type'
    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_program_type', False):
            types = self.env['op.program'].browse(self.env.context.get('program_id')).program_types
            return types.name_get()
        return super(OpProgramType, self).name_search(
            name, args, operator=operator, limit=limit)