from openerp import models, fields


class OpAuthor(models.Model):
    _name = 'op.author'

    name = fields.Char('Name', size=128, required=True)
    # address = fields.Many2one('res.partner', 'Address')
    street1 = fields.Char('Street 1')
    street2 = fields.Char('Street 2')
    city = fields.Char('City')
    country = fields.Char('Country')
    book_ids = fields.Many2many('op.book', string='Book(s)')
