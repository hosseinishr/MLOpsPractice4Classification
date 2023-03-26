##############################################################################
# Import necessary modules
# #############################################################################

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from constants import *
from mapping.significant_categorical_level import *
from mapping.city_tier_mapping import city_tier_mapping
import importlib.util

###############################################################################
# Define default arguments and create an instance of DAG
# ##############################################################################
def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

utils = module_from_file("utils", "/home/Assignment/airflow/dags/Lead_scoring_inference_pipeline/utils.py")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022,7,30),
    'retries' : 1, 
    'retry_delay' : timedelta(seconds=5)
}


Lead_scoring_inference_dag = DAG(
    dag_id = 'Lead_scoring_inference_pipeline',
    default_args = default_args,
    description = 'Inference pipeline of Lead Scoring system',
    schedule_interval = '@hourly',
    catchup = False
)

# Creating a task for load_data_into_db() with task id load_data_into_db
op_load_data_into_db = PythonOperator(task_id='load_data_into_db',
                                      python_callable=utils.load_data_into_db,
                                      op_kwargs={},
                                      dag=Lead_scoring_inference_dag)

# Creating a task for map_city_tier() with task id map_city_tier
op_map_city_tier = PythonOperator(task_id='map_city_tier',
                                  python_callable=utils.map_city_tier,
                                  op_kwargs={},
                                  dag=Lead_scoring_inference_dag)

# Creating a task for map_categorical_vars() with task id map_categorical_vars
op_map_categorical_vars = PythonOperator(task_id='map_categorical_vars',
                                         python_callable=utils.map_categorical_vars,
                                         op_kwargs={},
                                         dag=Lead_scoring_inference_dag)

# Creaitng a task for interactions_mapping() with taskk id interactions_mapping
op_interactions_mapping = PythonOperator(task_id='interactions_mapping',
                                         python_callable=utils.interactions_mapping,
                                         op_kwargs={},
                                         dag=Lead_scoring_inference_dag)

###############################################################################
# Create a task for encode_data_task() function with task_id 'encoding_categorical_variables'
# ##############################################################################
op_encoding_categorical_variables = PythonOperator(task_id='encoding_categorical_variables',
                                                   python_callable=utils.encode_features,
                                                   op_kwargs={},
                                                   dag=Lead_scoring_inference_dag)

###############################################################################
# Create a task for input_features_check() function with task_id 'checking_input_features'
# ##############################################################################
op_checking_input_features = PythonOperator(task_id='checking_input_features',
                                            python_callable=utils.input_features_check,
                                            op_kwargs={},
                                            dag=Lead_scoring_inference_dag)

###############################################################################
# Create a task for load_model() function with task_id 'generating_models_prediction'
# ##############################################################################
op_generating_models_prediction = PythonOperator(task_id='generating_models_prediction',
                                                 python_callable=utils.get_models_prediction,
                                                 op_kwargs={},
                                                 dag=Lead_scoring_inference_dag)

###############################################################################
# Create a task for prediction_col_check() function with task_id 'checking_model_prediction_ratio'
# ##############################################################################
op_checking_model_prediction_ratio = PythonOperator(task_id='checking_model_prediction_ratio',
                                                    python_callable=utils.prediction_ratio_check,
                                                    op_kwargs={},
                                                    dag=Lead_scoring_inference_dag)

###############################################################################
# Define relationship between tasks
# ##############################################################################
op_load_data_into_db >> op_map_city_tier >> op_map_categorical_vars >> op_interactions_mapping >> op_encoding_categorical_variables >> op_checking_input_features >> op_generating_models_prediction >> op_checking_model_prediction_ratio
