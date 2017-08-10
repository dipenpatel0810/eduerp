from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Genre(models.Model):
    _name = 'book_genre'
    _rec_name = 'genre'
    genre = fields.Char(string='Genre')

class OtherBooks(models.Model):
    _name = 'other_books'
    _rec_name = 'other'
    other = fields.Char(string='Type')
    book_ids_ref1 = fields.One2many('op.book' , 'other_books_ids1', string="Books")

class OpBook(models.Model):
    _name = 'op.book'

    name = fields.Char('Title', size=128, required=True)
    code = fields.Char('Code')
    isbn = fields.Char('ISBN Code', size=64)
    tags = fields.Many2many('op.tag', string='Tag(s)')
    author_ids = fields.Many2many('op.author', string='Author(s)')
    edition = fields.Char('Edition')
    description = fields.Text('Description')
    publisher_ids = fields.Many2many('op.publisher', string='Publisher(s)')
    movement_line = fields.One2many('op.book.movement', 'book_id', 'Movements')
    queue_ids = fields.One2many('op.book.queue', 'book_id', 'Book Queue')
    unit_ids = fields.One2many('op.book.unit', 'book_id', 'Units')
    book_type = fields.Selection([('Educational','Educational'),('Other','Other')],'Book Type')
    other_books_ids1 =  fields.Many2one('other_books', string='Type')
    genre_ids = fields.Many2many('book_genre', string="Genre")
    department_ids = fields.Many2many('op.department', string='Department')

    @api.multi
    def request_this_book(self):
        res = { 'name' : 'BookReqForm',
                'view_type' : 'form',
                'view_mode' : 'form,tree',
                'res_model' : 'op.book.queue',
                'type' : 'ir.actions.act_window',
                }
        return res

    _sql_constraints = [
        ('unique_name_isbn',
         'unique(isbn)',
         'ISBN code must be unique per book!'),
        ('unique_name_code',
         'unique(code)',
         'Internal Code must be unique per book!'),
    ]
