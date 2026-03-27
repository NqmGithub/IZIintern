from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_ids = fields.One2many('student', 'partner_id', string='Student Profiles')
    is_student_partner = fields.Boolean(
        string='Is Student Partner',
        compute='_compute_is_student_partner',
        store=True,
        index=True,
    )

    @api.depends('student_ids')
    def _compute_is_student_partner(self):
        for partner in self:
            partner.is_student_partner = bool(partner.student_ids)
