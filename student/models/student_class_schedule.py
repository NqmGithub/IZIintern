from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.orm.models import _

class StudentClassSchedule(models.Model):
    _name = 'student.class.schedule'
    _description = 'Student Class Schedule'
    _rec_name = 'class_id'

    class_id = fields.Many2one('student.class', string='Class', required=True)
    day_id = fields.Many2one('student.day.of.week', string='Day of Week', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)

    @api.constrains('start_time', 'end_time')
    def _check_time_range(self):
        for record in self:
            if record.end_time <= record.start_time:
                raise ValidationError(_('End Time must be greater than Start Time.'))
    