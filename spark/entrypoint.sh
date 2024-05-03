#!bin/bash

SPARK_WORKLOAD=$1

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

if [ "$SPARK_WORKLOAD" = "master" ]; 
then
    start-master.sh -p 7077 
#   echo "Starting Spark Master"
#   /spark/bin/spark-class org.apache.spark.deploy.master.Master
elif [ "$SPARK_WORKLOAD" = "worker" ]; 
then
    start-worker.sh spark://spark-master:7077
#   echo "Starting Spark Worker"
#   /spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
elif [ "$SPARK_WORKLOAD" = "history" ]; 
then
    start-history-server.sh
fi
else
  echo "Unknown workload"
fi