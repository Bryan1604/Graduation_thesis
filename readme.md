
Đề tài: phân tích và dữ lý dữ liệu trong cutomer data platfrom để 
    - xác định phân khúc khách hàng
    - đưa ra thông tin về hồ sơ khách hàng.

các thanhf phan chính:
- frontend : giao diện web bán hàng và snowplow
- backend : server của web bán hàng

- loader : thư mục chứa kafka để lưu trữ dữ liệu khi nhận được từ tracking
        -> sau đó có 2 hướng đi :
            +) từ kafka -> elastic search : để lưu trữ lâu dài và search ( kiểu lưu trữ sở thích dài hạn)
            +) kafka -> spark streaming : xử lý nhưng hành vi người dùng gần đây ( giống như kiểu sở thích ngắn hạn)

port :
- airflow : 8080
- 


Cac bươc thuc hien hien:
- Lay du lieu tu kafka lưu vao elasticsearch elasticsearch, từ elasticseach tính toán để lưu vào db

lý do ko chạy được postgress -> mount sai : ./snowplow/postgres-data:/var/lib/postgresql/data .
 Phải là : ./snowplow/postgres-data:/var/lib/postgresql@14/data
 Do tải xuống là bản postgresql@14 đổi tên từ postgresql :v