FROM apache/hadoop-runner  
ARG HADOOP_URL=https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV HADOOP_HOME=/opt/hadoop

WORKDIR /opt
RUN sudo rm -rf /opt/hadoop && curl -LSs -o hadoop.tar.gz $HADOOP_URL && \
    tar zxf hadoop.tar.gz && \
    rm hadoop.tar.gz && mv hadoop* hadoop && \
    rm -rf /opt/hadoop/share/doc && \
    wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz && \
    tar -xzf spark-3.5.1-bin-hadoop3.tgz
WORKDIR /opt/hadoop
ADD log4j.properties /opt/hadoop/etc/hadoop/log4j.properties
RUN sudo chown -R hadoop:users /opt/hadoop/etc/hadoop/*
