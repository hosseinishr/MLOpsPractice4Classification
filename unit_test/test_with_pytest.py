##############################################################################
# Import the necessary modules
##############################################################################


import pandas as pd
import os
import sqlite3
from sqlite3 import Error
from utils import *
import pytest
from significant_categorical_level import *
from city_tier_mapping import city_tier_mapping
from constants import *


###############################################################################
# Write test cases for load_data_into_db() function
# ##############################################################################

def test_load_data_into_db():
    """_summary_
    This function checks if the load_data_into_db function is working properly by
    comparing its output with test cases provided in the db in a table named
    'loaded_data_test_case'


    SAMPLE USAGE
        output=test_get_data()

    """
    build_dbs(DB_PATH, DB_FILENAME)

    load_data_into_db(DB_PATH, DB_FILENAME, DATA_DIRECTORY, RAW_DATA_FILENAME, LOADED_DATA_TABLENAME)
    
    # connection to the dbs
    conn_utils = sqlite3.connect(DB_PATH+DB_FILENAME)
    conn_reference = sqlite3.connect(DB_PATH+DB_REFERENCE_FILENAME)
    
    # read from dbs' tables
    df_utils = pd.read_sql('select * from ' + LOADED_DATA_TABLENAME, conn_utils)
    df_reference = pd.read_sql('select * from ' + LOADED_DATA_TABLENAME_REFERENCE, conn_reference)
    df_reference.rename(columns={"total_leads_droppped": "total_leads_dropped"}, inplace = True)
    
    df_equality_check_flag = df_utils.equals(df_reference)
    
    assert df_equality_check_flag == True , 'load_data_into_db not working properly!'

###############################################################################
# Write test cases for map_city_tier() function
# ##############################################################################
def test_map_city_tier():
    """_summary_
    This function checks if map_city_tier function is working properly by
    comparing its output with test cases provided in the db in a table named
    'city_tier_mapped_test_case'


    SAMPLE USAGE
        output=test_map_city_tier()

    """
    map_city_tier(DB_PATH, DB_FILENAME, city_tier_mapping, LOADED_DATA_TABLENAME, CITY_TIER_MAPPED_TABLENAME)
    
    # connection to the dbs
    conn_utils = sqlite3.connect(DB_PATH+DB_FILENAME)
    conn_reference = sqlite3.connect(DB_PATH+DB_REFERENCE_FILENAME)
    
    # read from dbs' tables
    df_utils = pd.read_sql('select * from ' + CITY_TIER_MAPPED_TABLENAME, conn_utils)
    df_reference = pd.read_sql('select * from ' + CITY_TIER_MAPPED_TABLENAME_REFERENCE, conn_reference)
    
    df_equality_check_flag = df_utils.equals(df_reference)
    
    assert df_equality_check_flag == True , 'map_city_tier not working properly!'
    
    
###############################################################################
# Write test cases for map_categorical_vars() function
# ##############################################################################    
def test_map_categorical_vars():
    """_summary_
    This function checks if map_cat_vars function is working properly by
    comparing its output with test cases provided in the db in a table named
    'categorical_variables_mapped_test_case'


    SAMPLE USAGE
        output=test_map_cat_vars()

    """
    map_categorical_vars(DB_PATH, DB_FILENAME, list_platform, list_medium, list_source, 
                         CITY_TIER_MAPPED_TABLENAME, CATEGORICAL_VARIABLES_MAPPED_TABLENAME)
    
    # connection to the dbs
    conn_utils = sqlite3.connect(DB_PATH+DB_FILENAME)
    conn_reference = sqlite3.connect(DB_PATH+DB_REFERENCE_FILENAME)
    
    # read from dbs' tables
    df_utils = pd.read_sql('select * from ' + CATEGORICAL_VARIABLES_MAPPED_TABLENAME, conn_utils)
    df_reference = pd.read_sql('select * from ' + CATEGORICAL_VARIABLES_MAPPED_TABLENAME_REFERENCE, conn_reference)
    
    df_equality_check_flag = df_utils.equals(df_reference)
    
    assert df_equality_check_flag == True , 'map_categorical_vars not working properly!'
    

###############################################################################
# Write test cases for interactions_mapping() function
# ##############################################################################    
def test_interactions_mapping():
    """_summary_
    This function checks if test_column_mapping function is working properly by
    comparing its output with test cases provided in the db in a table named
    'interactions_mapped_test_case'


    SAMPLE USAGE
        output=test_column_mapping()

    """ 
    interactions_mapping(DB_PATH, DB_FILENAME, CATEGORICAL_VARIABLES_MAPPED_TABLENAME, INDEX_COLUMNS, 
                         TARGET_COLUMN, INTERACTION_MAPPING_FILE, MODEL_INPUT_TABLENAME, SELECTED_FEATURES,
                         INTERACTIONS_MAPPED_TABLENAME)
    
    # connection to the dbs
    conn_utils = sqlite3.connect(DB_PATH+DB_FILENAME)
    conn_reference = sqlite3.connect(DB_PATH+DB_REFERENCE_FILENAME)
    
    # read from dbs' tables
    df_utils = pd.read_sql('select * from ' + INTERACTIONS_MAPPED_TABLENAME, conn_utils)
    df_reference = pd.read_sql('select * from ' + INTERACTIONS_MAPPED_TABLENAME_REFERENCE, conn_reference)
    
    df_equality_check_flag = df_utils.equals(df_reference)
    
    assert df_equality_check_flag == True , 'interactions_mapping not working properly!'
