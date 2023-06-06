from airflow import DAG

# Usually dag_id is the file name of the dag!
with DAG(dag_id='simple_dag') as dag:
    None
