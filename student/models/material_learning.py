from odoo import models, fields, api

class MaterialLearning(models.Model):
    _name = 'material.learning'
    _inherit = 'book'
    _description = 'Material Learning'

    learning_level = fields.Selection([
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('high', 'High'),
    ], string='Learning Level', default='primary')
    topic_type = fields.Selection([
        ('grammar', 'Grammar'),
        ('vocabulary', 'Vocabulary'),
        ('listening', 'Listening'),
        ('speaking', 'Speaking'),
        ('writing', 'Writing'),
    ], string='Topic Type', default='grammar')
    source = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External'),
    ], string='Source', default='internal')
    