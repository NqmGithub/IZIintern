from odoo import models, fields, api

class Book(models.Model):
    _name = 'book'
    _description = 'Book'

    name = fields.Char(string='Book Name', required=True)
    author = fields.Char(string='Author')
    publication_date = fields.Date(string='Publication Date')
    isbn = fields.Char(string='ISBN')