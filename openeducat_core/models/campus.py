from openerp import models, fields


class OpCampus(models.Model):
    _name = 'op.campus'

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=128, required=True)
    street = fields.Char('Street', size=256)
    street2 = fields.Char('Street2', size=256)
    phone = fields.Char('Phone', size=16)
    mobile = fields.Char('Mobile', size=16)
    email = fields.Char('Email', size=256)
    city = fields.Char('City', size=64)
    zip = fields.Char('Zip', size=8)
    state_id = fields.Many2one('res.country.state', 'States')
    country_id = fields.Many2one('res.country', 'Country')
    institute_ids = fields.One2many('op.institute', 'campus_id', string="Institutes")
    _sql_constraints = [
            ('id_unique',
             'UNIQUE(code)',
             "The campus id must be unique"),
    ]