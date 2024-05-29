# FROM python:3.11.1

# # Cài đặt Java, Scala và Apache Spark
# RUN apt-get update && \
#     apt-get install -y default-jdk && \
#     apt-get install -y scala && \
#     wget https://downloads.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz && \
#     tar -xvzf spark-3.4.3-bin-hadoop3.tgz && \
#     mv spark-3.4.3-bin-hadoop3 /opt/spark && \
#     rm spark-3.4.3-bin-hadoop3.tgz

# # Cài đặt các thư viện Python cần thiết cho ứng dụng Spark Streaming
# RUN pip install pyspark kafka-python  # Thêm các thư viện khác nếu cần

# # Thiết lập biến môi trường để Apache Spark có thể tìm thấy Java
# ENV JAVA_HOME /usr/lib/jvm/default-java

# # Thiết lập biến môi trường để Apache Spark có thể tìm thấy Scala
# ENV SCALA_HOME /usr/share/scala

# # Thiết lập biến môi trường để Apache Spark có thể tìm thấy Spark
# ENV SPARK_HOME /opt/spark

# # Thiết lập biến môi trường để Python có thể tìm thấy PySpark
# ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip

# # Thiết lập biến môi trường để Apache Spark có thể tìm thấy Python
# ENV PYSPARK_PYTHON python3

# # Thiết lập thư mục làm việc cho ứng dụng Spark Streaming
# WORKDIR /app

# # Copy code của ứng dụng Spark Streaming vào hình ảnh
# COPY ./spark/spark_streaming.py /app/spark_streaming.py

FROM apache/airflow

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev openjdk-17-jdk && \
    apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark kafka-python psutil