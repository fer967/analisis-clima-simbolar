from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath("/opt/airflow/scripts"))

from ingest import ingest_data
from clean_data import clean_data
from transform_data import transform_data
from load_to_postgres import load_to_postgres


with DAG(
    dag_id="clima_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    task_ingest = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data
    )

    task_clean = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data
    )

    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )
    
    task_load = PythonOperator(
    task_id="load_to_postgres",
    python_callable=load_to_postgres
    )

    task_ingest >> task_clean >> task_transform >> task_load