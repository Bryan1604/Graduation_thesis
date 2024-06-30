import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    dag_id = "process_one_segment",
    default_args = {
        "owner": "LuongVu",
        "start_date": datetime(2024,6,3,0,0),
        "retries": 5,
        "retry_delay" : timedelta(minutes = 1)
    },
    schedule_interval = '@hourly',
    catchup=False
)

process_one_segment = BashOperator(
    task_id='process_one_segment',
    bash_command='docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 2g \
    --conf spark.cores.max=2 \
    --packages mysql:mysql-connector-java:8.0.28 \
    jobs/segments/process_one_segment.py',
    dag=dag,
)

process_one_segment
