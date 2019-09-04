from airflow.contrib.operators import KubernetesOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.contrib.kubernetes.pod import Port


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
    'smline', default_args=default_args, schedule_interval=timedelta(minutes=500))

passing = KubernetesPodOperator(namespace='default',
                          image="gcr.io/blume-platform-data-nw-nonprod/rpamanager",
                          cmds=["python","/SM/long_scrape_sm.py"],
                          labels={"airflow1": "smline"},
                          name="smline",
                          task_id="smline",
                          get_logs=True,
                          dag=dag
                          )
