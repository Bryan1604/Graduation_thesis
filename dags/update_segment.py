import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

dag = DAG(
    dag_id = "update_segment",
    default_args = {
        "owner": "LuongVu",
        "start_date": datetime(2024,6,3,0,0),
        "retries": 5,
        "retry_delay" : timedelta(minutes = 1)
    },
    schedule_interval = '@hourly',
    catchup=False
)

process_segment = BashOperator(
    task_id='process_segment',
    bash_command='docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --packages mysql:mysql-connector-java:8.0.28 jobs/segments/process_segment.py',
    dag=dag,
)

process_segment