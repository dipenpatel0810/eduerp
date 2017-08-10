from openerp import models, fields, api


class OpBookPurchase(models.Model):
    _name = 'op.book.purchase'
    _inherit = 'mail.thread'
    _description = 'Book Purchase Request'

    name = fields.Char('Title', size=128, required=True)
    author = fields.Char(
        'Author(s)', size=256, required=True, track_visibility='onchange')
    edition = fields.Char('Edition')
    publisher = fields.Char('Publisher(s)', size=256)
    course_ids = fields.Many2one(
        'op.course', 'Course', required=True, track_visibility='onchange')
    subject_ids = fields.Many2one(
        'op.subject', 'Subject', required=True, track_visibility='onchange')
    requested_id = fields.Many2one(
        'res.partner', 'Requested By',
        default=lambda self: self.env['res.partner'].search(
            [('user_id', '=', self.env.uid)]))
    state = fields.Selection(
        [('draft', 'Draft'), ('request', 'Requested'), ('reject', 'Rejected'),
         ('accept', 'Accepted')], 'State', select=True, readonly=True,
        default='draft', track_visibility='onchange')

    @api.one
    def act_requested(self):
        self.state = 'request'

    @api.one
    def act_accept(self):
        self.state = 'accept'

    @api.one
    def act_reject(self):
        self.state = 'reject'
