import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

dag = DAG(
    dag_id = "sparking_flow",
    default_args = {
        "owner": "LuongVu",
        "start_date": airflow.utils.dates.days_ago(1)
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

process_long_hobbies = SparkSubmitOperator(
    task_id = "process_long_hobbies",
    conn_id = "spark-connect",
    application = "jobs/process_long_hobbies.py",
    # total_executor_cores='2',
    # executor_cores='2',
    # executor_memory='1g',
    # num_executors='2',
    # driver_memory='1g',
    dag = dag
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)
start >> process_long_hobbies >> end