# FROM python:3.11.1-bullseye as spark-base

# ARG SPARK_VERSION=3.5.1

# RUN apt-getupdate && \
#     apt-get install -y --no--install-recommends \
#     sudo\
#     curl \
#     vim \
#     unzip \
#     rsync \
#     openjdk-17-jdk \
#     build-essential \
#     software-properties-common \
#     ssh && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# ENV SPARK_HOME = ${SPARK_HOME:-"/opt/spark"}
# ENV HADOOP_HOME = ${HADOOP_HOME:-"/opt/hadoop"}

# RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
# WORKDIR ${SPARK_HOME}

# RUN curl -s https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.3.tgz \
#     && tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.3.tgz --directory /opt/spark --strip-components 1 \
#     && rm -rf spark-${SPARK_VERSION}-bin-hadoop3.3.tgz

# COPY requirements/requirements.txt .
# RUN pip3 install -r requirements.txt

# ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
# ENV SPARK_HOME="/opt/spark"
# ENV SPARk_MASTER="spark://spark-master:7077"
# ENV SPARk_MASTER_HOST spark-master
# ENV SPARK_MASTER_PORT 7077
# ENV PYSPARK_PYTHON python3

# COPY conf/spark-defaults.conf "${SPARK_HOME}/conf"

# RUN chmod u+x /opt/spark/sbin/* && \
#     chmod u+x /opt/spark/bin/*

# ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

# COPY entrypoint.sh .

# ENTRYPOINT [ "./entrypoint.sh" ]

FROM openjdk:17-jdk

# Cài đặt Python và PySpark
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pyspark

# Cài đặt Spark
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3.3
ENV SPARK_PACKAGE=spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV SPARK_HOME=/opt/${SPARK_PACKAGE}

RUN wget -qO- https://downloads.apache.org/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz | tar xvz -C /opt && \
    ln -s ${SPARK_HOME} /opt/spark && \
    rm -rf ${SPARK_HOME}/examples ${SPARK_HOME}/data

ENV PATH=$PATH:${SPARK_HOME}/bin
