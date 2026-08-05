from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


def run_smoke_test() -> None:
    print("RetailPulse Airflow smoke test passed")


with DAG(
    dag_id="retailpulse_smoke",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["retailpulse", "smoke"],
) as dag:
    smoke_task = PythonOperator(
        task_id="run_smoke_test",
        python_callable=run_smoke_test,
    )
