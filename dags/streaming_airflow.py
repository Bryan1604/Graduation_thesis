import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

dag = DAG(
    dag_id = "Streaming_flow",
    default_args = {
       "owner": "LuongVu",
        "start_date": datetime(2024,6,3,0,0),
        "retries": 5,
        "retry_delay" : timedelta(minutes = 5)
    },
    schedule_interval = "@daily"
)

start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"),
    dag=dag
)

# segment_job = SparkSubmitOperator(
#     task_id = "segment_job",
#     conn_id = "spark-conn",
#     application = "jobs/segments/process_segment.py",
#     dag = dag
# )

# process_long_hobbies = SparkSubmitOperator(
    # task_id = "process_long_hobbies",
    # conn_id = "spark-connect",
    # application = "jobs/process_long_hobbies.py",
    # packages = "mysql:mysql-connector-java:8.0.28",
    # total_executor_cores='2',
    # executor_cores='2',
    # executor_memory='1g',
    # num_executors='2',
    # driver_memory='1g',
    # dag = dag
# )

# process_segment = SparkSubmitOperator(
#     task_id = "process_segment",
#     conn_id = "spark-conn",
#     name="process_segment",
#     application = "/usr/local/spark/jobs/segments/process_segment.py",
#     packages = 'mysql:mysql-connector-java:8.0.28',
#     dag = dag,
#     verbose=1,
#     # spark_binary="/opt/bitnami/spark/bin/spark-submit",
#     conf={
#         "spark.master": "spark://spark-master:7077",
#     }
# )

# chay realtime
# process_favorite_category = BashOperator(
#     task_id='process_favorite_category',
#     bash_command='docker exec spark-master spark-submit \
#     --master spark://spark-master:7077 \
#     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
#     jobs/process_favorite_category.py',
#     dag=dag,
# )

# --conf spark.scheduler.pool=streaming \
process_event_streaming = BashOperator(
    task_id='process_event_streaming',
    bash_command="""
        docker exec spark-master spark-submit \
        --master spark://spark-master:7077 \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark_streaming.py
    """,
)

process_event_streaming = BashOperator(
    task_id='process_event_streaming',
    bash_command='docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark_streaming.py',
)


end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)
start >> process_event_streaming >> end