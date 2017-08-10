from openerp import models, fields, api, _

unit_states = [('available', 'Available'), ('issue', 'Issued'),
               ('reserve', 'Reserved'), ('lost', 'Lost')]


class OpBookUnit(models.Model):
    _name = 'op.book.unit'
    _inherit = 'mail.thread'
    _description = 'Book Unit'

    name = fields.Char('Name')
    book_id = fields.Many2one('op.book', 'Book', required=True, track_visibility='onchange')
    code = fields.Char('Code')
    barcode = fields.Char('Barcode', size=20)
    hello_piyu = fields.Boolean('naam mein kya hai',default=False)
    movement_lines = fields.One2many(
        'op.book.movement', 'book_unit_id', 'Movements')
    state = fields.Selection(
        unit_states, 'State', default='available', track_visibility='onchange')


    _sql_constraints = [
        ('unique_name_barcode',
         'unique(barcode)',
         'Barcode must be unique per book unit!'),
    ]

    @api.onchange('book_id')
    def onchange_book(self):
        self.code = self.book_id.code
        self.hello_piyu=True
        # print "piyu" , self.code
        if self.code:
            print "qqq" , self.hello_piyu
            ccode = self.code
            self.name = ccode + self.env['ir.sequence'].next_by_code('op.book.unit')

    _defaults={
                      'name': lambda obj, cr, uid, context: '/',
                        
               }   
    @api.model
    def name_search(self, name, args=None,operator='iLike',limit=100):
        if self.env.context.get('get_available_books', False):
            lst = []
            lst.append(self.env.context.get('book_id'))
            book_unit = self.env['op.book.unit'].search([('book_id','in',lst),('state','=','available')])
            return book_unit.name_get()
        return super(OpBookMovement, self).name_search(
            name, args, operator=operator, limit=limit)
