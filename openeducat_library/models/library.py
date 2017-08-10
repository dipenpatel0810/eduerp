from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpLibraryCardType(models.Model):
    _name = 'op.library.card.type'
    _description = 'Library Card Type'

    name = fields.Char('Name', size=256, required=True)
    card_code = fields.Char('Code')
    allow_book = fields.Integer('No of Books Allowed', size=10, required=True)
    duration = fields.Integer(
        'Duration', help='Duration in terms of Number of Lead Days',
        required=True)
    penalty_amt_per_day = fields.Float('Penalty Amount per Day', required=True)

    @api.constrains('allow_book', 'duration', 'penalty_amt_per_day')
    def check_details(self):
        if self.allow_book < 0 or self.duration < 0.0 or \
                self.penalty_amt_per_day < 0.0:
            raise ValidationError(_('Enter proper value'))


class OpLibraryCard(models.Model):
    _name = 'op.library.card'
    _rec_name = 'number'
    _description = 'Library Card'

    number = fields.Char('Number')
    library_card_type_id = fields.Many2one(
        'op.library.card.type', 'Card Type', required=True)
    issue_date = fields.Date(
        'Issue Date', required=True, default=fields.Date.today())
    type = fields.Selection(
        [('student', 'Student'), ('faculty', 'Faculty')],
        'User', required=True)
    student_id = fields.Many2one('op.student', 'Student')
    faculty_id = fields.Many2one('op.faculty', 'Faculty')
    student_faculty_name = fields.Char('Name')

    @api.model 
    def create(self,values):
        # libname = self.env['op.library.card'].search([('student_id.user_default','=',self.user_default.id)]).id
        # print "###################################",libname
        res = super(OpLibraryCard,self).create(values)
        res.student_id.library_card_id = res.id
        
        return res


    @api.onchange('faculty_id')
    def onchange_faculty_id(self):
        self.student_faculty_name = self.faculty_id.name
        
    @api.onchange('student_id')
    def onchange_student_id(self):
        self.student_faculty_name = self.student_id.name

    @api.onchange('library_card_type_id')
    def onchange_librarycard(self):
        if (self.library_card_type_id.name == 'Faculty'):
            self.type = 'faculty'
        elif (self.library_card_type_id.name == 'Student'):
            self.type = 'student'
        #first we would check that value is not False in card_code and sequence and then execute the concatenation
        if self.library_card_type_id.card_code and self.env['ir.sequence'].next_by_code('op.library.card'):
            libcode = self.library_card_type_id.card_code
            self.number = libcode + self.env['ir.sequence'].next_by_code('op.library.card')
    _defaults={
                      'number': lambda obj, cr, uid, context: '/',
                        
               }

    _sql_constraints = [
        ('unique_library_card_number',
         'unique(number)', 'Library card Number should be unique per card!'),
    ]
