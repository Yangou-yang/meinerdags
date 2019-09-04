# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This is an example dag for using the Kubernetes Executor.
"""
import os

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, BashOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='smexecute', default_args=args,
    schedule_interval=None
)

affinity = {
    'podAntiAffinity': {
        'requiredDuringSchedulingIgnoredDuringExecution': [
            {
                'topologyKey': 'kubernetes.io/hostname',
                'labelSelector': {
                    'matchExpressions': [
                        {
                            'key': 'app',
                            'operator': 'In',
                            'values': ['airflow']
                        }
                    ]
                }
            }
        ]
    }
}

tolerations = [{
    'key': 'dedicated',
    'operator': 'Equal',
    'value': 'airflow'
}]


def print_stuff():  # pylint: disable=missing-docstring
    print("stuff!")


def use_zip_binary():
    """
    Checks whether Zip is installed.
    :return: True if it is installed, False if not.
    :rtype: bool
    """
    return_code = os.system("zip")
    assert return_code == 0


cleanup_task = BashOperator(
        task_id='task_1_data_file_cleanup'
        ,bash_command="python /SM/long_scrape_sm.py"
        ,dag=dag,
        executor_config={"KubernetesExecutor": {"image": "gcr.io/blume-platform-data-nw-nonprod/rpamanager"}}
    )

cleanup_task