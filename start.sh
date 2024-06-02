#!/bin/bash

# Start SSH service
service ssh start

export HADOOP_OPTS="$HADOOP_OPTS --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.lang.reflect=ALL-UNNAMED --add-opens java.base/java.net=ALL-UNNAMED"

if [ "$1" == "namenode" ]; then
    # export HADOOP_OPTS="$HADOOP_OPTS --add-opens java.base/java.lang=ALL-UNNAMED"
    $HADOOP_HOME/bin/hdfs namenode
elif [ "$1" == "datanode" ]; then
    # export HADOOP_OPTS="$HADOOP_OPTS --add-opens java.base/java.lang=ALL-UNNAMED"
    $HADOOP_HOME/bin/hdfs datanode
elif [ "$1" == "resourcemanager" ]; then
    # export HADOOP_OPTS="$HADOOP_OPTS --add-opens java.base/java.lang=ALL-UNNAMED"
    $HADOOP_HOME/bin/yarn resourcemanager
elif [ "$1" == "nodemanager" ]; then
    # export HADOOP_OPTS="$HADOOP_OPTS --add-opens java.base/java.lang=ALL-UNNAMED"
    $HADOOP_HOME/bin/yarn nodemanager
elif [ "$1" == "spark-master" ]; then
    export SPARK_MASTER_OPTS="$SPARK_MASTER_OPTS --add-opens java.base/java.lang=ALL-UNNAMED"
    $SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master
elif [ "$1" == "spark-worker" ]; then
    export SPARK_WORKER_OPTS="$SPARK_WORKER_OPTS --add-opens java.base/java.lang=ALL-UNNAMED"
    $SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
else
    echo "Unknown service: $1"
    exit 1
fi
