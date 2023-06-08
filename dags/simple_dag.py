from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago


default_args = {
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
}


def downloading_data(**kwargs):
    print(kwargs)


with DAG(dag_id='simple_dag', default_args=default_args, start_date=days_ago(5),
         schedule_interval='@daily',
         catchup=True,
         max_active_runs=2) as dag:

    downloading_data = PythonOperator(
        task_id='downloading_data',
        python_callable=downloading_data
    )
