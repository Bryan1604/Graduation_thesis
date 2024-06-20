import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

dag = DAG(
    dag_id = "batch_processing",
    default_args = {
        "owner": "LuongVu",
        "start_date": datetime(2024,6,3,0,0),
        "retries": 5,
        "retry_delay" : timedelta(minutes = 1)
    },
    schedule_interval = "0 0 * * *",
    catchup=False
)

start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"),
    dag=dag
)

process_old_favorite_category = BashOperator(
    task_id='process_old_favorite_category',
    bash_command='docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 2g \
    --conf spark.cores.max=2 \
    jobs/process_old_favorite_category.py',
    dag=dag,
)

process_long_hobbies = BashOperator(
    task_id='process_long_hobbies',
    bash_command='docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --executor-memory 2g \
    --conf spark.cores.max=2 \
    jobs/process_long_hobbies.py',
    dag=dag,
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)
start >> process_old_favorite_category >> process_long_hobbies >> end