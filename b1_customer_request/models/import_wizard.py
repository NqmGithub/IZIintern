from email.mime import base
import io
from odoo import models, fields, api
from odoo.tools.xml_utils import BytesIO
import openpyxl;
import base64

class CustomerRequestImportWizard(models.TransientModel):
    _name = 'customer.request.import.wizard'
    _description = 'Customer Request Import Wizard'

    excel_file = fields.Binary(string='Excel File', required=True)
    file_name = fields.Char(string='File Name')

    def action_import_requests(self):
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
                error_msg.append(f"Product with ID {product_id} not found.")
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
                'name': 'Import Errors',
                'view_mode': 'form',
                'res_model': 'customer.request.import.error.wizard',
                'target': 'new',
                'context': {'default_error_message': '\n'.join(error_msg)},
            }

        return { 'type': 'ir.actions.act_window_close' }
