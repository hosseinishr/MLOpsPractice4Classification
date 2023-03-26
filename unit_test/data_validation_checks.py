# importing necessary libraries and modules

import pandas as pd
import sqlite3
from sqlite3 import Error
from Assignment.data_pipeline.scripts.schema import *


"""
Define function to validate raw data's schema
############################################################################## 
"""


def raw_data_schema_check(DB_PATH, DB_FILENAME, raw_data_schema, DATA_DIRECTORY, RAW_DATA_FILENAME):
    '''
    This function check if all the columns mentioned in schema.py are present in
    leadscoring.csv file or not.

   
    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be   
        raw_data_schema : schema of raw data in the form of a list/tuple as present 
                          in 'schema.py'

    OUTPUT
        If the schema is in line then prints 
        'Raw datas schema is in line with the schema present in schema.py' 
        else prints
        'Raw datas schema is NOT in line with the schema present in schema.py'

    
    SAMPLE USAGE
        raw_data_schema_check
    '''
    # read the leadscoring data
    df_lead_scoring = pd.read_csv(DATA_DIRECTORY+RAW_DATA_FILENAME, index_col=[0])
    
    if set(raw_data_schema) == set(list(df_lead_scoring.columns)):
        print('Raw datas schema is in line with the schema present in schema.py')
    else:
        print('Raw datas schema is NOT in line with the schema present in schema.py')

###############################################################################
# Define function to validate model's input schema
# ############################################################################## 

def model_input_schema_check(DB_PATH, DB_FILENAME, model_input_schema, MODEL_INPUT_TABLENAME):
    '''
    This function check if all the columns mentioned in model_input_schema in 
    schema.py are present in table named in 'model_input' in db file.

   
    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be   
        model_input_schema : schema of models input data in the form oa list/tuple
                          present as in 'schema.py'

    OUTPUT
        If the schema is in line then prints 
        'Models input schema is in line with the schema present in schema.py'
        else prints
        'Models input schema is NOT in line with the schema present in schema.py'
    
    SAMPLE USAGE
        raw_data_schema_check
    '''
    # connection to the db
    conn = sqlite3.connect(DB_PATH+DB_FILENAME)

    # read from db table
    df_lead_scoring = pd.read_sql('select * from ' + MODEL_INPUT_TABLENAME, conn)
    
    if set(model_input_schema) == set(list(df_lead_scoring.columns)):
        print('Models input schema is in line with the schema present in schema.py')
    else:
        print('Models input schema is NOT in line with the schema present in schema.py')

    
    
