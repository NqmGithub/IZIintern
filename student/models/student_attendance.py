from odoo import models, fields, api

class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'

    student_id = fields.Many2one('student', string='Student', required=True)
    date = fields.Date(string='Date', required=True)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ], string='Status', default='present')
    homework_status = fields.Selection([
        ('completed', 'Completed'),
        ('not_completed', 'Not Completed'),
        ('late', 'Late'),
    ], string='Homework Status', default='not_completed')