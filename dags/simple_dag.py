from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.models.baseoperator import chain, cross_downstream


default_args = {
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': True,
    'email': 'abc@dfg.com'
}


def _downloading_data(**kwargs):
    with open('/tmp/my_file.txt', 'w') as f:
        f.write('my_data')
    return 42


def _checking_data(ti):
    my_xcom = ti.xcom_pull(key='return value', task_ids=['downloading_data'])
    print(my_xcom)


def _failure(context):
    print('I am a failure handler on callback')
    print(context)


with DAG(dag_id='simple_dag', default_args=default_args, start_date=days_ago(2),
         schedule_interval='@daily',
         catchup=True,
         max_active_runs=2) as dag:

    downloading_data = PythonOperator(
        task_id='downloading_data',
        python_callable=_downloading_data
    )

    checking_data = PythonOperator(
        task_id='checking_data',
        python_callable=_checking_data
    )

    waiting_data = FileSensor(
        task_id='waiting_data',
        fs_conn_id='fs_default',
        filepath='my_file.txt',
        poke_interval=5
    )

    processing_data = BashOperator(
        task_id='processing_data',
        bash_command='exit 0',
        on_failure_callback=_failure
    )

    # downloading_data.set_downstream(waiting_data)
    # waiting_data.set_downstream(processing_data)

    # processing_data.set_upstream(waiting_data)
    # waiting_data.set_upstream(downloading_data)

    # chain(downloading_data, [waiting_data, processing_data])

    # cross_downstream([downloading_data, checking_data],
    #                  [waiting_data, processing_data])

    downloading_data >> waiting_data >> checking_data >> processing_data
