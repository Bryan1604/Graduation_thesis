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
    --executor-memory 2g \
    --conf spark.cores.max=2 \
    --packages mysql:mysql-connector-java:8.0.28 \
    jobs/segments/process_segment.py',
    dag=dag,
)

# def process_one_segment(segment_id):
#     spark_submit_command = f"docker exec spark-master spark-submit \
#         --master spark://spark-master:7077 \
#         --executor-memory 2g \
#         --conf spark.cores.max=2 \
#         --packages mysql:mysql-connector-java:8.0.28 \
#         jobs/segments/process_one_segment.py --segment_id {segment_id}"
#     return BashOperator(
#         task_id=f'process_one_segment_{segment_id}',
#         bash_command=spark_submit_command,
#         dag=dag,
#     )
    
# process_one_segment(segment_id)


# process_one_segment = BashOperator(
#     task_id='process_one_segment',
#     bash_command='docker exec spark-master spark-submit \
#     --master spark://spark-master:7077 \
#     --executor-memory 2g \
#     --conf spark.cores.max=2 \
#     --packages mysql:mysql-connector-java:8.0.28 \
#     jobs/segments/process_one_segment.py',
#     dag=dag,
# )

process_segment