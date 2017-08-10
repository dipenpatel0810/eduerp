from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class Roomtype(models.Model):
    _name = 'hostel.roomtype'
    name = fields.Char('Room type')

class OpHostel(models.Model):
    _name = 'op.hostel'

    name = fields.Char('Name', size=16, required=True)
    capacity = fields.Integer('Hostel Capacity', required=True)
    hostel_room_lines = fields.One2many(
        'op.hostel.room', 'hostel_id', 'Room(s)')
    hostel_type = fields.Selection(
        [('1','College Hostel'), ('2', 'Private Hostel')],
        'Hostel Type', required=True)
    room_type = fields.Many2many('hostel.roomtype', string= "Room type")

    pstreet = fields.Char('Street', size=256)
    pstreet2 = fields.Char('Street2', size=256)
    pphone = fields.Char('Phone', size=16)
    pmobile = fields.Char('Mobile', size=16)
    pcity = fields.Char('City', size=64)
    pzip = fields.Char('Zip', size=8)
    pstate_id = fields.Many2one('res.country.state', string='States')
    pcountry_id = fields.Many2one('res.country', string='Country')

    @api.one
    @api.constrains('hostel_room_lines')
    def _check_hostel_capacity(self):
        if self.capacity <= 0:
            raise ValidationError(_('Enter proper Hostel Capacity'))
        counter = 0.00
        for room in self.hostel_room_lines:
            counter += room.students_per_room
            if counter > self.capacity:
                raise ValidationError(_('Hostel Capacity Over'))
