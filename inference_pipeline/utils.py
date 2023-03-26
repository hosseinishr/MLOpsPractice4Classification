'''
filename: utils.py
functions: encode_features, load_model
creator: shashank.gupta
version: 1
'''

# #############################################################################
# Import necessary modules and files
# #############################################################################

import mlflow
import mlflow.sklearn
import pandas as pd
import os
import sqlite3
import logging
from sqlite3 import Error
from datetime import datetime
from mapping.significant_categorical_level import *
from mapping.city_tier_mapping import city_tier_mapping
from constants import *


###############################################################################
# Define function to load the csv file to the database
# ##############################################################################

#def load_data_into_db(DB_PATH, DB_FILENAME, DATA_DIRECTORY, INFERENCE_DATA_FILENAME, LOADED_DATA_TABLENAME):
def load_data_into_db():    
    '''
    Thie function loads the data present in data directiry into the db
    which was created previously.
    It also replaces any null values present in 'toal_leads_dropped' and
    'referred_lead' with 0.


    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        data_directory : path of the directory where 'leadscoring.csv' 
                        file is present
        

    OUTPUT
        Saves the processed dataframe in the db in a table named 'loaded_data'.
        If the table with the same name already exsists then the function 
        replaces it.


    SAMPLE USAGE
        load_data_into_db()
    '''
    # connection to the db
    conn = sqlite3.connect(DB_PATH+DB_FILENAME)
    
    # read the leadscoring data
    df_lead_scoring_inf = pd.read_csv(DATA_DIRECTORY+INFERENCE_DATA_FILENAME)
    
    # removing columns: 'Unnamed: 0'
    df_lead_scoring_inf = df_lead_scoring_inf[[col for col in df_lead_scoring_inf.columns 
                                               if col not in USELESS_COLUMN]]
    
    # replacing any null values present in 'toal_leads_dropped' and
    # 'referred_lead' with 0.
    df_lead_scoring_inf["total_leads_dropped"] = df_lead_scoring_inf["total_leads_dropped"].fillna(0)
    df_lead_scoring_inf["referred_lead"] = df_lead_scoring_inf["referred_lead"].fillna(0)
    
    # writing to the db
    df_lead_scoring_inf.to_sql(name=LOADED_DATA_TABLENAME, con=conn, if_exists='replace', index=False)
    
    conn.close()
    

###############################################################################
# Define function to map cities to their respective tiers
# ##############################################################################

#def map_city_tier(DB_PATH, DB_FILENAME, city_tier_mapping, LOADED_DATA_TABLENAME, CITY_TIER_MAPPED_TABLENAME):    
def map_city_tier():
    '''
    This function maps all the cities to their respective tier as per the
    mappings provided in /mappings/city_tier_mapping.py file. If a
    particular city's tier isn't mapped in the city_tier_mapping.py then
    the function maps that particular city to 3.0 which represents
    tier-3.


    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        city_tier_mapping : a dictionary that maps the cities to their tier

    
    OUTPUT
        Saves the processed dataframe in the db in a table named
        'city_tier_mapped'. If the table with the same name already 
        exsists then the function replaces it.

    
    SAMPLE USAGE
        map_city_tier()

    '''
    # connection to the db
    conn = sqlite3.connect(DB_PATH+DB_FILENAME)

    # read from db table
    df_lead_scoring_inf = pd.read_sql('select * from ' + LOADED_DATA_TABLENAME, conn)
    
    # map city tier
    df_lead_scoring_inf["city_tier"] = df_lead_scoring_inf["city_mapped"].map(city_tier_mapping)
    df_lead_scoring_inf["city_tier"] = df_lead_scoring_inf["city_tier"].fillna(3.0)
    df_lead_scoring_inf = df_lead_scoring_inf.drop(['city_mapped'], axis = 1)
    
    # writing to the db
    df_lead_scoring_inf.to_sql(name=CITY_TIER_MAPPED_TABLENAME, con=conn, if_exists='replace', index=False)
    
    conn.close()

###############################################################################
# Define function to map insignificant categorial variables to "others"
# ##############################################################################


#def map_categorical_vars(DB_PATH, DB_FILENAME, list_platform, list_medium, list_source, CITY_TIER_MAPPED_TABLENAME, CATEGORICAL_VARIABLES_MAPPED_TABLENAME):
def map_categorical_vars():
    '''
    This function maps all the insignificant variables present in 'first_platform_c'
    'first_utm_medium_c' and 'first_utm_source_c'. The list of significant variables
    should be stored in a python file in the 'significant_categorical_level.py' 
    so that it can be imported as a variable in utils file.
    

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        list_platform : list of all the significant platform.
        list_medium : list of all the significat medium
        list_source : list of all the significant source

        **NOTE : list_platform, list_medium & list_source are all constants and
                 must be stored in 'significant_categorical_level.py'
                 file. The significant levels are calculated by taking top 90
                 percentils of all the levels. For more information refer to
                 'data_cleaning.ipynb' notebook.
  

    OUTPUT
        Saves the processed dataframe in the db in a table named
        'categorical_variables_mapped'. If the table with the same name already 
        exsists then the function replaces it.

    
    SAMPLE USAGE
        map_categorical_vars()
    '''
    # connection to the db
    conn = sqlite3.connect(DB_PATH+DB_FILENAME)

    # read from db table
    df_lead_scoring = pd.read_sql('select * from ' + CITY_TIER_MAPPED_TABLENAME, conn)
    
    # processing first_platform_c
    new_df = df_lead_scoring[~df_lead_scoring['first_platform_c'].isin(list_platform)]
    new_df['first_platform_c'] = "others"
    old_df = df_lead_scoring[df_lead_scoring['first_platform_c'].isin(list_platform)]
    df = pd.concat([new_df, old_df])
    
    # processing first_utm_medium_c
    new_df = df[~df['first_utm_medium_c'].isin(list_medium)]
    new_df['first_utm_medium_c'] = "others"
    old_df = df[df['first_utm_medium_c'].isin(list_medium)]
    df = pd.concat([new_df, old_df])
    
    # processing first_utm_source_c
    new_df = df[~df['first_utm_source_c'].isin(list_source)]
    new_df['first_utm_source_c'] = "others"
    old_df = df[df['first_utm_source_c'].isin(list_source)]
    df = pd.concat([new_df, old_df])
    
    # writing to the db
    df.to_sql(name=CATEGORICAL_VARIABLES_MAPPED_TABLENAME, con=conn, if_exists='replace', index=False)
    
    conn.close()


##############################################################################
# Define function that maps interaction columns into 4 types of interactions
# #############################################################################
#def interactions_mapping(DB_PATH, DB_FILENAME, CATEGORICAL_VARIABLES_MAPPED_TABLENAME, INDEX_COLUMNS, TARGET_COLUMN, INTERACTION_MAPPING_FILE, MODEL_INPUT_TABLENAME, SELECTED_FEATURES, INTERACTIONS_MAPPED_TABLENAME):
def interactions_mapping():
    '''
    This function maps the interaction columns into 4 unique interaction columns
    These mappings are present in 'interaction_mapping.csv' file. 


    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        interaction_mapping_file : path to the csv file containing interaction's
                                   mappings
        index_columns : list of columns to be used as index while pivoting and
                        unpivoting
        NOTE : Since while inference we will not have 'app_complete_flag' which is
        our label, we will have to exculde it from our index_columns. It is recommended 
        that you use an if loop and check if 'app_complete_flag' is present in 
        'categorical_variables_mapped' table and if it is present pass a list with 
        'app_complete_flag' in it as index_column else pass a list without 'app_complete_flag'
        in it.

    
    OUTPUT
        Saves the processed dataframe in the db in a table named 
        'interactions_mapped'. If the table with the same name already exsists then 
        the function replaces it.
        
        It also drops all the features that are not requried for training model and 
        writes it in a table named 'model_input'

    
    SAMPLE USAGE
        interactions_mapping()
    '''
    # connection to the db
    conn = sqlite3.connect(DB_PATH+DB_FILENAME)
    
    # read from db table
    df = pd.read_sql('select * from ' + CATEGORICAL_VARIABLES_MAPPED_TABLENAME, conn)
    
    # preparing the index_column list
    #index_columns = index_columns[:7]
    index_column = INDEX_COLUMNS
    if TARGET_COLUMN in df.columns:
        index_column += [TARGET_COLUMN]
        
    # dropping the duplicates
    df = df.drop_duplicates()
    
    # reading the interaction mapping file
    df_event_mapping = pd.read_csv(INTERACTION_MAPPING_FILE, index_col=[0])
    
    # pivoting and unpivoting
    df_unpivot = pd.melt(df, id_vars=index_column, var_name='interaction_type', value_name='interaction_value')
    df_unpivot['interaction_value'] = df_unpivot['interaction_value'].fillna(0)
    df = pd.merge(df_unpivot, df_event_mapping, on='interaction_type', how='left')
    df = df.drop(['interaction_type'], axis=1)
    df_pivot = df.pivot_table(values='interaction_value', index=index_column, columns='interaction_mapping', 
                              aggfunc='sum')
    df_pivot = df_pivot.reset_index()
    
    # dropping all the features that are not requried for training model
    final_features = [col for col in df_pivot.columns if col in SELECTED_FEATURES]
    df_final = df_pivot[final_features]
    
    # writing to the db
    df_final.to_sql(name=MODEL_INPUT_TABLENAME, con=conn, if_exists='replace', index=False)
    df_pivot.to_sql(name=INTERACTIONS_MAPPED_TABLENAME, con=conn, if_exists='replace', index=False)
    
    conn.close()
    

###############################################################################
# Define the function to train the model
# ##############################################################################


#def encode_features(DB_PATH, DB_FILENAME, MODEL_INPUT_TABLENAME, ONE_HOT_ENCODED_FEATURES, 
#                    FEATURES_TO_ENCODE, DF_FEATURES_INF_TABLENAME):
def encode_features():        
    '''
    This function one hot encodes the categorical features present in our  
    training dataset. This encoding is needed for feeding categorical data 
    to many scikit-learn models.

    INPUTS
        db_file_name : Name of the database file 
        db_path : path where the db file should be
        ONE_HOT_ENCODED_FEATURES : list of the features that needs to be there in the final encoded dataframe
        FEATURES_TO_ENCODE: list of features  from cleaned data that need to be one-hot encoded
        **NOTE : You can modify the encode_featues function used in heart disease's inference
        pipeline for this.

    OUTPUT
        1. Save the encoded features in a table - features

    SAMPLE USAGE
        encode_features()
    '''
    # read the model input data
    cnx = sqlite3.connect(DB_PATH+DB_FILENAME)
    df_model_input = pd.read_sql('select * from ' + MODEL_INPUT_TABLENAME, cnx)

    # create df to hold encoded data and intermediate data
    df_encoded = pd.DataFrame(columns=ONE_HOT_ENCODED_FEATURES)
    df_placeholder = pd.DataFrame()

    # encode the features using get_dummies()
    for feature in FEATURES_TO_ENCODE:
        if feature in df_model_input.columns:
            encoded = pd.get_dummies(df_model_input[feature])
            encoded = encoded.add_prefix(feature + '_')
            df_placeholder = pd.concat([df_placeholder, encoded], axis=1)

    # add the encoded features into a single dataframe
    for feature in df_encoded.columns:
        if feature in df_model_input.columns:
            df_encoded[feature] = df_model_input[feature]
        if feature in df_placeholder.columns:
            df_encoded[feature] = df_placeholder[feature]
    df_encoded.fillna(0, inplace=True)

    # save the features and target in separate tables
    df_features = df_encoded
    df_features.to_sql(name=DF_FEATURES_INF_TABLENAME, con=cnx, if_exists='replace', index=False)

    cnx.close()
    
###############################################################################
# Define the function to check the columns of input features
# ##############################################################################
   

def input_features_check():
    '''
    This function checks whether all the input columns are present in our new
    data. This ensures the prediction pipeline doesn't break because of change in
    columns in input data.

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        ONE_HOT_ENCODED_FEATURES: List of all the features which need to be present
        in our input data.

    OUTPUT
        It writes the output in a log file based on whether all the columns are present
        or not.
        1. If all the input columns are present then it logs - 'All the models input are present'
        2. Else it logs 'Some of the models inputs are missing'

    SAMPLE USAGE
        input_col_check()
    '''
    # read the input data
    cnx = sqlite3.connect(DB_PATH+DB_FILENAME)
    df = pd.read_sql('select * from ' + DF_FEATURES_INF_TABLENAME, cnx)

    # check if all columns are present
    if set(df.columns) == set(ONE_HOT_ENCODED_FEATURES):
        print('All the models input are present')
    else:
        print('Some of the models inputs are missing')
    
    
###############################################################################
# Define the function to load the model from mlflow model registry
# ##############################################################################

def get_models_prediction():
    '''
    This function loads the model which is in production from mlflow registry and 
    uses it to do prediction on the input dataset. Please note this function will the load
    the latest version of the model present in the production stage. 

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be
        model from mlflow model registry
        model name: name of the model to be loaded
        stage: stage from which the model needs to be loaded i.e. production


    OUTPUT
        Store the predicted values along with input data into a table

    SAMPLE USAGE
        load_model()
    '''
    # ensure DB_FILE_MLFLOW = 'Lead_scoring_mlflow_production.db' is created in the same folder beforehand 
    
    # MLFLOW run is still running from training phase, not new from here!!
    
    # set the tracking uri
    mlflow.set_tracking_uri(TRACKING_URI)

    # load the latest model from production stage
    loaded_model = mlflow.pyfunc.load_model(
        model_uri=f"models:/{MODEL_NAME}/{STAGE}")

    # read the new data
    cnx = sqlite3.connect(DB_PATH+DB_FILENAME)
    df_new_data = pd.read_sql('select * from ' + DF_FEATURES_INF_TABLENAME, cnx)

    # run the model to generate the prediction on new data
    y_pred = loaded_model.predict(df_new_data)
    df_new_data['app_complete_flag_pred'] = y_pred

    # store the data in a table
    df_new_data.to_sql(name=DF_PRED_TABLENAME, con=cnx, if_exists='replace', index=False)
    cnx.close()

###############################################################################
# Define the function to check the distribution of output column
# ##############################################################################

def prediction_ratio_check():
    '''
    This function calculates the % of 1 and 0 predicted by the model and  
    and writes it to a file named 'prediction_distribution.txt'.This file 
    should be created in the ~/airflow/dags/Lead_scoring_inference_pipeline 
    folder. 
    This helps us to monitor if there is any drift observed in the predictions 
    from our model at an overall level. This would determine our decision on 
    when to retrain our model.
    

    INPUTS
        db_file_name : Name of the database file
        db_path : path where the db file should be

    OUTPUT
        Write the output of the monitoring check in prediction_distribution.txt with 
        timestamp.

    SAMPLE USAGE
        prediction_col_check()
    '''
    # read the input data
    cnx = sqlite3.connect(DB_PATH+DB_FILENAME)
    df = pd.read_sql('select * from ' + DF_PRED_TABLENAME, cnx)

    # get the distribution of categories in prediction col
    value_counts = df['app_complete_flag_pred'].value_counts(normalize=True)

    # write the output in a file
    ct = datetime.now()
    st = str(ct)+' %of 1 = ' + \
        str(value_counts[1])+' %of 2 ='+str(value_counts[0])
    with open(PRED_DIST_FILE_PATH+'prediction_distribution.txt', 'a') as f:
        f.write(st+"\n")
   