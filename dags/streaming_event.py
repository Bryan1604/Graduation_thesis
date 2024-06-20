import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

dag = DAG(
    dag_id = "streaming_event",
    default_args = {
        "owner": "LuongVu",
        "start_date": datetime(2024,6,3,0,0),
        "retries": 5,
        "retry_delay" : timedelta(minutes = 5)
    },
    schedule_interval = "0 0 * * *",
    catchup=False
)

start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"),
    dag=dag
)

# chay realtime
process_favorite_category = BashOperator(
    task_id='process_favorite_category',
    bash_command='docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 2g \
    --conf spark.cores.max=2 \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
    jobs/process_favorite_category.py',
    dag=dag,
)

# --conf spark.scheduler.pool=streaming \
process_event_streaming = BashOperator(
    task_id='process_event_streaming',
    bash_command="""
        docker exec spark-master spark-submit \
        --master spark://spark-master:7077 \
        --executor-memory 2g \
        --conf spark.cores.max=2 \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
        jobs/spark_streaming.py
    """,
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)


start >> [process_event_streaming,process_favorite_category] >> end
# [process_favorite_category,process_event_streaming]