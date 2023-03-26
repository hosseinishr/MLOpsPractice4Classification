##############################################################################
# Import necessary modules
# #############################################################################
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta
from constants import *
import os
import sqlite3
from sqlite3 import Error
import pandas as pd
import importlib.util


###############################################################################
# Define default arguments and DAG
# ##############################################################################

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

utils = module_from_file("utils", "/home/Assignment/airflow/dags/Lead_scoring_training_pipeline/utils.py")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022,7,30),
    'retries' : 1, 
    'retry_delay' : timedelta(seconds=5)
}


ML_training_dag = DAG(
                dag_id = 'Lead_scoring_training_pipeline',
                default_args = default_args,
                description = 'Training pipeline for Lead Scoring System',
                schedule_interval = '@monthly',
                catchup = False
)

###############################################################################
# Create a task for encode_features() function with task_id 'encoding_categorical_variables'
# ##############################################################################
op_encoding_categorical_variables = PythonOperator(task_id='encoding_categorical_variables',
                                                   python_callable=utils.encode_features,
                                                   op_kwargs={},
                                                   dag=ML_training_dag)
###############################################################################
# Create a task for get_trained_model() function with task_id 'training_model'
# ##############################################################################
op_training_model = PythonOperator(task_id='training_model',
                                   python_callable=utils.get_trained_model,
                                   op_kwargs={},
                                   dag=ML_training_dag)

###############################################################################
# Define relations between tasks
# ##############################################################################
op_encoding_categorical_variables >> op_training_model
