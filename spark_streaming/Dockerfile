# Use an appropriate base image
FROM --platform=linux/amd64 bitnami/spark:3.5

# Set environment variables
ENV SPARK_HOME=/opt/bitnami/spark

# Copy the Spark Streaming script into the container
COPY spark_streaming.py /opt/bitnami/spark/spark_streaming/spark_streaming.py

# Install any required Python packages
COPY requirements.txt /opt/bitnami/spark/requirements.txt
RUN pip3 install -r /opt/bitnami/spark/requirements.txt

# Command to run the Spark Streaming script
CMD ["/opt/bitnami/spark/bin/spark-submit", "--master", "spark://spark-master:7077", "/opt/bitnami/spark/spark_streaming/spark_streaming.py"]
