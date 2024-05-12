FROM bitnami/spark:latest

# Cài đặt thư viện elasticsearch bằng pip
COPY requirements.txt /requirements.txt
RUN pip install mysql-connector-python==8.4.0
RUN pip install mysql-connector==2.2.9
RUN pip install -r /requirements.txt
