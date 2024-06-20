# Use base image bitnami/spark with amd64 platform
FROM --platform=linux/amd64 bitnami/spark:3.5

# Set environment variables
ENV SPARK_HOME=/opt/bitnami/spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV IVY_HOME=/opt/bitnami/spark/.ivy2

# Set working directory
WORKDIR /opt/bitnami/spark

# Install required packages
USER root
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y openssh-server

# Copy requirements.txt and install Python libraries
COPY requirements.txt /opt/bitnami/spark/requirements.txt
RUN pip3 install --upgrade pip && pip install -r /opt/bitnami/spark/requirements.txt

# Install the required package
RUN /opt/bitnami/scripts/spark/run.sh --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0

# Copy jobs directory
COPY ./jobs /opt/bitnami/spark/jobs

# Create .ivy2 directory if it doesn't exist
RUN mkdir -p $IVY_HOME

# Set entrypoint command
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]
