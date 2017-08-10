from openerp import models, fields, api

class CasteCategory(models.Model):
    _name = 'caste.category'
    name = fields.Char('Caste Name',required=True)
    code= fields.Char('Code', required=True)
    stu_ids = fields.One2many('op.student','caste', string="Student of this Caste")