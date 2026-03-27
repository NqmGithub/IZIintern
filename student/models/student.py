from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.orm.models import _
class Student(models.Model):
    _name='student'
    _inherits={'res.partner':'partner_id'}

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    dob = fields.Date(string='Date of Birth')
    english_experience = fields.Selection([
        ('none', 'None'),
        ('basic', 'Basic'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], string='English Experience', default='none')
    parents_contact = fields.Char(string='Parents Contact')
    class_id = fields.Many2one('student.class', string='Class')
    is_student = fields.Boolean(string='Is Student', default=True)

    @api.constrains('parents_contact')
    def _check_parents_contact(self):
        for student in self:
            if student.parents_contact and not student.parents_contact.isdigit():
                raise ValidationError(_('Parents Contact must contain only digits.'))
            
    @api.constrains('dob')
    def _check_dob(self):
        for student in self:
            if student.dob and student.dob > fields.Date.today():
                raise ValidationError(_('Date of Birth cannot be in the future.'))