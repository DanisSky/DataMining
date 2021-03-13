import datetime as dt

from airflow.example_dags.tutorial import default_args
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=3),
    'depends_on_past': False,
    'start_date': dt.datetime(2021, 3, 13)
}
dag = DAG(
    'collect_dag',
    default_args=default_args,
    description='DAG',
    schedule_interval=None,
    start_date=days_ago(3),
    tags=['vkParser'],
)

BashOperator(
    task_id='main_task',
    bash_command='python3 /opt/DataMining/VkParser/main.py',
    dag=dag
)
