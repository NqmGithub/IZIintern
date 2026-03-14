from email.mime import base
import io
from math import e
from odoo.addons.im_livechat.controllers import attachment
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.xml_utils import BytesIO
import openpyxl;
import base64

class CustomerRequestImportWizard(models.TransientModel):
    _name = 'customer.request.import.wizard'
    _description = 'Customer Request Import Wizard'

    excel_file = fields.Binary(string='Excel File')
    file_name = fields.Char(string='File Name')

    def download_template(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/b1_customer_request/static/src/request_template.xlsx',
            'target': 'self',
        }
    
    def action_import_requests(self):
        if not self.excel_file:
            raise UserError(_("Please upload an Excel file."))
        file_content = base64.b64decode(self.excel_file)
        workbook = openpyxl.load_workbook(io.BytesIO(file_content))
        sheet = workbook.active

        lead_id = self.env.context.get('active_id')
        lead = self.env['crm.lead'].browse(lead_id)
        
        request_data = []
        error_msg = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            product_id = row[0]
            description = row[1]
            date = row[2]
            quantity = row[3]

            product = self.env['product.template'].search([('id', '=', product_id)], limit=1)
            if not product:
                error_msg.append(_("Product with ID %s not found.") % product_id)
                continue
            request_data.append((0, 0, {
                'product_id': product.id,
                'description': description,
                'date': date,
                'quantity': quantity,
            }))

        lead.write({'request_ids': request_data})
        if error_msg:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Import Errors'),
                'view_mode': 'form',
                'res_model': 'customer.request.import.error.wizard',
                'target': 'new',
                'context': {'default_error_message': '\n'.join(error_msg)},
            }

        return { 'type': 'ir.actions.act_window_close' }

class CustomerRequestImportErrorWizard(models.TransientModel):
    _name = 'customer.request.import.error.wizard'
    _description = 'Customer Request Import Error Wizard'

    error_message = fields.Text(string='Error Message', readonly=True)

    def download_error(self):
        filename = "import_errors.txt"
        error_content = self.error_message.encode('utf-8')
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(error_content),
            'mimetype': 'text/plain',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

