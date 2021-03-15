import datetime as dt

import airflow
from airflow.example_dags.tutorial import default_args
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=2),
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
}
dag = DAG(
    'collect_dag',
    default_args=default_args,
    description='DAG',
    schedule_interval=None,
    tags=['vkParser'],
    template_searchpath="/opt/DataMining/VkParser",
)

BashOperator(
    task_id='main_task',
    bash_command='python3 main.py',
    dag=dag,
)
