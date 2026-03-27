from odoo import models, fields, api

class StudentClassSchedule(models.Model):
    _name = 'student.class.schedule'
    _description = 'Student Class Schedule'

    class_id = fields.Many2one('student.class', string='Class', required=True)
    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day of Week', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    