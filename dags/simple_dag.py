from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta


# Usually dag_id is the file name of the dag!
with DAG(dag_id='simple_dag', start_date=datetime(2023, 1, 1),
         schedule_interval=timedelta(hours=7)) as dag:

    task_1 = DummyOperator(task_id='task_1')
