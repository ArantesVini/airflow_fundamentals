from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago


default_args = {
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
}


def _downloading_data(**kwargs):
    with open('/tmp/my_file.txt', 'w') as f:
        f.write('my_data')


with DAG(dag_id='simple_dag', default_args=default_args, start_date=days_ago(5),
         schedule_interval='@daily',
         catchup=True,
         max_active_runs=2) as dag:

    downloading_data = PythonOperator(
        task_id='downloading_data',
        python_callable=_downloading_data
    )

    waiting_data = FileSensor(
        task_id='waiting_data',
        fs_conn_id='fs_default',
        filepath='my_file.txt',
        poke_interval=5
    )

    testing_task = PythonOperator(
        task_id='testing_task',
        python_callable=lambda: print('testing task')
    )
