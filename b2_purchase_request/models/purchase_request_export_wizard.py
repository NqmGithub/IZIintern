import base64
import io

import xlsxwriter

from odoo import _, fields, models
from odoo.exceptions import UserError

class PurchaseRequestExportWizard(models.TransientModel):
    _name = 'purchase.request.export.wizard'
    _description = 'Purchase Request Export Wizard'

    file_name = fields.Char(string='File Name', default='purchase_requests.xlsx')
    include_department = fields.Boolean(string='Include Department', default=True)
    include_requester = fields.Boolean(string='Include Requester', default=True)
    include_approver = fields.Boolean(string='Include Approver', default=True)
    include_date = fields.Boolean(string='Include Request Date', default=True)
    include_date_approved = fields.Boolean(string='Include Approval Date', default=True)
    include_description = fields.Boolean(string='Include Description', default=True)
    include_state = fields.Boolean(string='Include Status', default=True)
    include_total_quantity = fields.Boolean(string='Include Total Quantity', default=True)
    include_total_amount = fields.Boolean(string='Include Total Amount', default=True)
    include_canceled_reason = fields.Boolean(string='Include Reason for Cancellation', default=True)

    def export_purchase_requests(self):
        active_ids = self.env.context.get('active_ids', [])
        purchase_requests = self.env['purchase.request'].browse(active_ids)

        filename = self.file_name + '.xlsx'
        
        data = []
        for request in purchase_requests:
            row = {}
            if self.include_department:
                row['Department'] = request.department_id.name
            if self.include_requester:
                row['Requester'] = request.requester_id.name
            if self.include_approver:
                row['Approver'] = request.approver_id.name
            if self.include_date:
                row['Request Date'] = request.date
            if self.include_date_approved:
                row['Approval Date'] = request.date_approved
            if self.include_description:
                row['Description'] = request.description
            if self.include_state:
                row['Status'] = dict(request._fields['state'].selection).get(request.state, '')
            if self.include_total_quantity:
                row['Total Quantity'] = request.total_quantity
            if self.include_total_amount:
                row['Total Amount'] = request.total_amount
            if self.include_canceled_reason:
                row['Reason for Cancellation'] = request.canceled_reason
            data.append(row)
        
        if not data:
            raise UserError(_('No data to export. Please select at least one purchase request and ensure it has data to export.'))
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Purchase Requests')
        
        headers = list(data[0].keys()) 
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header)

        for row_num, row_data in enumerate(data, start=1):
            for col_num, value in enumerate(row_data.values()):
                sheet.write(row_num, col_num, value)

        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(output.read()).decode('utf-8')
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': file_data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }