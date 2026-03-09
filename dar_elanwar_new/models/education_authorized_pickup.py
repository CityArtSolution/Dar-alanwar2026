from odoo import models, fields


class EducationAuthorizedPickup(models.Model):
    _name = 'education.authorized.pickup'
    _description = 'Authorized Pickup Person'

    student_id = fields.Many2one('education.student', string='Student',
                                  required=True, ondelete='cascade')
    name = fields.Char(string='Full Name', required=True)
    relation = fields.Char(string='Relation')
    phone = fields.Char(string='Phone')
    id_number = fields.Char(string='ID Number')
    photo = fields.Binary(string='Photo', attachment=True)
