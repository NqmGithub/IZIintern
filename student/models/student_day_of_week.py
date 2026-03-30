from odoo import models, fields, api

class StudentDayOfWeek(models.Model):
    _name = 'student.day.of.week'
    _description = 'Student Day of Week'

    name = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Day of Week', required=True)