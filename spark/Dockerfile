FROM bitnami/spark:latest

ENV SPARK_HOME /opt/bitnami/spark

# Cài đặt thư viện elasticsearch bằng pip
# Install Python packages
COPY spark/requirements.txt /opt/bitnami/spark/requirements.txt
RUN pip3 install -r /opt/bitnami/spark/requirements.txt

# Copy the entire app folder to the container
COPY jobs /opt/bitnami/spark/jobs

ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", "--master", "spark://spark-master:7077", "/opt/bitnami/spark/jobs/wordcount.py"]