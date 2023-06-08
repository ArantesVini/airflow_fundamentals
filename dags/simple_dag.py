from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago


with DAG(dag_id='simple_dag', start_date=days_ago(5),
         schedule_interval='@daily',
         catchup=True,
         max_active_runs=2) as dag:

    task_1 = DummyOperator(task_id='task_1')
