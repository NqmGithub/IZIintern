from odoo import models, fields
from odoo.orm.models import _

class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'
    _rec_name = 'student_id'
    _sql_constraints = [
        (
            'student_schedule_date_unique',
            'unique(student_id, schedule_id, date)',
            'Attendance already exists for this student, schedule, and date.',
        ),
    ]

    student_id = fields.Many2one('student', string='Student', required=True)
    schedule_id = fields.Many2one('student.class.schedule', string='Class Schedule', required=True)
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

    def mark_as_present(self):
        for record in self:
            record.status = 'present'

    def mark_as_absent(self):
        for record in self:
            record.status = 'absent'
    
    def mark_as_late(self):
        for record in self:
            record.status = 'late'
    
    def mark_homework_completed(self):
        for record in self:
            record.homework_status = 'completed'
            
    def mark_homework_not_completed(self):
        for record in self:
            record.homework_status = 'not_completed'

    def mark_homework_late(self):
        for record in self:
            record.homework_status = 'late'

    def action_generate_daily_attendance(self):
        today = fields.Date.context_today(self)
        day_index = str(today.weekday())
        weekday_labels = {
            '0': 'monday',
            '1': 'tuesday',
            '2': 'wednesday',
            '3': 'thursday',
            '4': 'friday',
            '5': 'saturday',
            '6': 'sunday',
        }
        expected_weekday_label = weekday_labels[day_index]

        all_schedules = self.env['student.class.schedule'].search([])
        schedules = all_schedules.filtered(
            lambda s: s.day_id and (
                str(s.day_id.name) == day_index
                or str(s.day_id.name).lower() == expected_weekday_label
            )
        )

        if not schedules:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Schedules Found'),
                    'message': _('No class schedules are configured for today.'),
                    'type': 'warning',
                    'sticky': False,
                },
            }

        created_count = 0
        for schedule in schedules:
            students = schedule.class_id.student_ids
            if not students and schedule.class_id.student_selection_ids:
                students = schedule.class_id.student_selection_ids
                students.filtered(lambda s: not s.class_id).write({'class_id': schedule.class_id.id})
            for student in students:
                existing_attendance = self.search([
                    ('student_id', '=', student.id),
                    ('schedule_id', '=', schedule.id),
                    ('date', '=', today),
                ], limit=1)
                if not existing_attendance:
                    self.create({
                        'student_id': student.id,
                        'schedule_id': schedule.id,
                        'date': today,
                    })
                    created_count += 1
        return{
            'name': 'Today\'s Attendance',
            'type': 'ir.actions.act_window',
            'res_model': 'student.attendance',
            'view_mode': 'list',
            'domain': [('date', '=', today)],
            'context': {
                'generated_schedule_count': len(schedules),
                'generated_attendance_count': created_count,
            },
            'target': 'current',
        }