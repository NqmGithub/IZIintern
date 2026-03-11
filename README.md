# namModules

## Ngày 1:
- Set up các công cụ, hệ thống odoo, tạo thử module đầu tiên và đọc tài liệu, đề bài lộ trình

## Ngày 2:
Bài 1
- Tạo được model customer.request với các trường theo yêu cầu của đề bài
- Tạo được menu, giao diện list, form cho customer.request 
- Bổ sung được trường request_ids, sale_amount (doanh số) và revenue (doanh thu) vào crm.lead với doanh số và doanh thu được tính theo yêu cầu đề bài
- Thêm được menu tới customer.request trong giao diện opportunity
- Thêm ngăn cách hành động thêm, sửa, xóa với customer.request trong ir.model.access.csv
- Thêm thông báo khóa hành động thêm/sửa/xóa với opportunity không còn new
- Vướng mắc: chưa chỉnh cho các trường trong opportunity thành readonly được (nhưng vẫn chặn được edit)
- Công việc còn lại của bài 1: tạo bảng giá và làm các yêu cầu bổ sung

## Ngày 3:
Bài 1
- Chỉnh sửa được chức năng bảng giá đẩy thông tin customer.request vào
- Thêm chức năng import customer.request từ excel ở trong lead
- Tạo được API tạo lead gồm đủ thông tin như trong đề bài
- Bài 1 cơ bản đã xong
Bài 2 
- Tạo được models của purchase.request và purchase.request.line 
- Thêm menu xem danh sách purchase request