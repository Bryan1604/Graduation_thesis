
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

- Lệnh chạy trên spark spark: vd
    docker exec -it spark-master spark-submit \
    --master spark://spark-master:7077 \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark_streaming.py

    docker exec -it spark-master spark-submit \
    --master spark://spark-master:7077 \
    --packages mysql:mysql-connector-java:8.0.28 jobs/segments/process_segment.py

Note :
    Done:
        - sao chép db
        - tải lên elasticseacrh
        - cập nhật sở thích dài hạn
        - cập nhật view count
        - xu ly cac don dat hang -> lay luon trong database cu khi co 1 don duoc dat của người dùng : total_purchase, total_purchase_value, avg_purchase_value, min_purchase_value
        - api segment, UI segment
        - sua lai API lay thong tin khach hang ( thong tin cac san pham yeu thich),
        - su ly du lieu date ( birthday)
        - loc theo nhieu dieu kien
        - spark streaming và đẩy dữ liệu lên elastic search
        - xử lý thông tin về sở thích ngắn hạn  ===> nen de la 1,2,3,4      
        - Xoa cac the loai yeu thich cu ( co thoi gian update qua 3 ngay truoc do)

    inprogress :  
        - CONFIG AIRFLOW (UU TIEN CAO NHAT)
        - xoá nhưng thể loại không có cập nhât ( trong 3 ngay gan nhat) (tạo API,..  hay dung nhu long_hobbies)
        - connect voi database mysql spark (??), su dung package cho spark-mysql
        - Loc theo dieu kien include
        - can chuong trinh theo doi hoat dong chay lien tuc  => khi khoi chay may chu spark -> cho chay luon ?? => deu can submit len spark ( co nen su dung file.sh)

        
        
    Can lam luon :

        - Khi co segment duoc tao moi hoac xoa -> goi toi airlow de chay code tao moi 1 segment

    todo :
        - sua lai API lay thong tin khach hang ( the loai yeu thich)
        - them 1 truong update_time vao bang customer_product -> cap nhat thoi gian xem san pham cua nguoi dung ( chưa biết có cần thiết không)
        - cap nhap the loai ma nguoi dung quan tam nhieu nhat
        - tạo segment theo thói quen mua sắm
        - tao segment theo  các sản phẩm quan tâm ( su dung include theo id ? ten san pham)
        - segment theo tinhf trạng khách hàng
        - segment dựa theo tương tác của khách hàng 
        - segment dựa theo hành vi của khách hàng
        link : https://blog.hub-js.com/segment-linh-hoat-tren-extech/

        - connect airflow voi spark
        - thi thoang kafka1  bị down đột ngột

       
    Điều kiện phân khúc được lưu dưới dạng json ??
     {
        field: "", : lưu thông tin về tên điều kiện 
        operator: "", lưu thông tin về kiểu giá trị 
        type: "", lưu thông tin về toán tử
        value: "", lưu thông tin về giá trị
     }


-- connect airflow voi spark-master bang ssh key
- tao ssh key trong airflow , khoa coong khai duoc luu vao  file /home/airflow/.ssh/id_rsa.pub
- truy cap vao docker spark master de sao chep khoa cong khai vua tao vao file authorized_keys
    docker exec -it spark-master /bin/bash
    mkdir -p ~/.ssh
    echo "your_public_key_content" >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    chmod 700 ~/.ssh
- tai ssh server tren docker spark-master, khoi dong ssh server : service ssh start
- truy cap tu airflow : ssh root@spark-master


các xử lý cần được chạy liên tục
- Spark_streaming 
- process_favorite_category
- process_product_view
Chương trình xử lý batch , lập lịch hàng ngày :
- process_long_hobbies
- process_old_favorite_category
- process_segment