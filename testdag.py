from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'testdag', default_args=default_args, schedule_interval=timedelta(minutes=500))

passing = KubernetesPodOperator(namespace='default',
                          image="nginx",
                          labels={"airflow1": "nginx"},
                          name="nginxtest",
                          task_id="nginxtest",
                          get_logs=True,
                          dag=dag
                          )