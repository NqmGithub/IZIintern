import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)

class StudentClass(models.Model):
    _name = 'student.class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'class_code'
    _description = 'Student Class'
    _student_count_warning_threshold = 2
    
    class_code = fields.Char(string='Class Code', required=True, copy=False, readonly=True, default=lambda self: 'New')
    class_location = fields.Selection([
        ('branch_a', 'Branch A'),
        ('branch_b', 'Branch B'),
        ('branch_c', 'Branch C'),
        ('online', 'Online'),
    ], string='Class Location')
    student_ids = fields.One2many('student', 'class_id', string='Students')
    student_selection_ids = fields.Many2many('student', string='Select Students',
                                            compute='_compute_student_selection_ids',
                                            inverse='_inverse_student_selection_ids')
    student_count = fields.Integer(string='Student Count', compute='_compute_student_count')
    class_type = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('high', 'High'),
    ], string='Class Type', default='primary')
    class_schedule = fields.One2many('student.class.schedule', 'class_id', string='Class Schedule')
    @api.depends('student_ids')
    def _compute_student_selection_ids(self):
        for record in self:
            record.student_selection_ids = record.student_ids

    def _inverse_student_selection_ids(self):
        for record in self:
            record.student_ids = record.student_selection_ids

    @api.depends('student_ids')
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('class_code', 'New') == 'New':
                loc = vals.get('class_location', 'branch_a')
                prefix = "A"
                match loc:
                    case 'branch_a':
                        prefix = "A"
                    case 'branch_b':
                        prefix = "B"
                    case 'branch_c':
                        prefix = "C"
                    case 'online':
                        prefix = "O"
                
                sequence_num = self.env['ir.sequence'].next_by_code('student.class.seq') or '0000'
                vals['class_code'] = f"{prefix}{sequence_num}"

        return super(StudentClass, self).create(vals_list)
    
    def _check_student_count_notification(self):
        activity_type = self.env.ref('mail.mail_activity_data_warning')
        model_id = self.env['ir.model']._get_id('student.class')
        records = self if self else self.search([])
        over_threshold = 0
        created_count = 0
        for record in records:
            if record.student_count > self._student_count_warning_threshold:
                over_threshold += 1
                existing_activity = self.env['mail.activity'].search([
                    ('res_id', '=', record.id),
                    ('res_model_id', '=', model_id),
                    ('activity_type_id', '=', activity_type.id),
                ], limit=1)
                if not existing_activity:
                    assigned_user = record.create_uid if record.create_uid and not record.create_uid.share else self.env.user
                    self.env['mail.activity'].create({
                        'res_id': record.id,
                        'res_model_id': model_id,
                        'activity_type_id': activity_type.id,
                        'user_id': assigned_user.id,
                        'automated': False,
                        'date_deadline': fields.Date.today(),
                        'summary': f'Student count exceeds {self._student_count_warning_threshold}',
                        'note': (
                            f'The class {record.class_code} has {record.student_count} students '
                            f'(threshold: {self._student_count_warning_threshold}).'
                        ),
                    })
                    created_count += 1
        return {
            'processed': len(records),
            'over_threshold': over_threshold,
            'created': created_count,
            'threshold': self._student_count_warning_threshold,
        }
