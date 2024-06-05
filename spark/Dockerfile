# Sử dụng base image bitnami/spark với nền tảng amd64
FROM --platform=linux/amd64 bitnami/spark:3.5

# Thiết lập biến môi trường
ENV SPARK_HOME=/opt/bitnami/spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV IVY_HOME=/opt/bitnami/spark/.ivy2
ENV SPARK_MASTER=yarn://namenode:8020
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
# Thiết lập thư mục làm việc
WORKDIR /opt/bitnami/spark

# Sử dụng quyền sudo để tạo thư mục và cập nhật các gói
USER root
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y openssh-server

# Sao chép tệp requirements.txt vào container và cài đặt các thư viện Python cần thiết
COPY requirements.txt /opt/bitnami/spark/requirements.txt
RUN pip3 install --upgrade pip && pip install -r /opt/bitnami/spark/requirements.txt

# Sao chép thư mục jobs vào container
# COPY ./jobs /opt/bitnami/spark/jobs

# Tạo thư mục .ivy2 nếu chưa tồn tại
RUN mkdir -p $IVY_HOME

# Thiết lập lệnh khởi động
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]

# Default command to run the Spark master with required packages
CMD ["/opt/bitnami/scripts/spark/run.sh", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2"]
