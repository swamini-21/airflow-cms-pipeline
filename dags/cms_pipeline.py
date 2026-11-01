from datetime import timedelta

from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator
from pendulum import datetime
import logging

def notify_failure(context):
    ti = context["task_instance"]
    logging.getLogger("airflow.task").error(
        "ALERT: task %s in DAG %s failed (run %s, try %s)",
        ti.task_id, ti.dag_id, context.get("run_id"), ti.try_number,
    )


@dag(
    dag_id="cms_pipeline",
    schedule=None,
    start_date=datetime(2026, 10, 30),
    catchup=False,
    default_args={
    "retries": 2, "retry_delay": timedelta(minutes=2), "on_failure_callback": notify_failure,},
    tags=["cms"],
)
def cms_pipeline():
    ingest = BashOperator(
        task_id="ingest",
        bash_command="cd /usr/local/airflow/cms_project && python -m ingestion.ingest",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "export DBT_ENGINE_MANAGE_STATE=false && "
            "cd /usr/local/airflow/cms_project/dbt/cms_dbt && "
            "/usr/local/airflow/dbt_venv/bin/dbt build --profiles-dir ."
        ),
    )

    soda_check = BashOperator(
        task_id="soda_check",
        bash_command=(
            "cd /usr/local/airflow/cms_project/soda && "
            "/usr/local/airflow/soda_venv/bin/soda scan "
            "-d cms_postgres -c configuration.airflow.yml checks.yml"
        ),
    )

    ingest >> dbt_build >> soda_check


cms_pipeline()