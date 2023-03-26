##############################################################################
# Import necessary modules and files
# #############################################################################


import pandas as pd
import os
import sqlite3
from sqlite3 import Error
from significant_categorical_level import *
from city_tier_mapping import city_tier_mapping

###############################################################################
# Define the function to build database
# ##############################################################################

def build_dbs(DB_PATH, DB_FILENAME):
    '''
    This function checks if the db file with specified name is present 
    in the /Assignment/01_data_pipeline/scripts folder. If it is not present it creates 
    the db file with the given name at the given path. 


    INPUTS
        db_file_name : Name of the database file 'utils_output.db'
        db_path : path where the db file should be '   


    OUTPUT
    The function returns the following under the conditions:
        1. If the file exsists at the specified path
                prints 'DB Already Exsists' and returns 'DB Exsists'

        2. If the db file is not present at the specified loction
                prints 'Creating Database' and creates the sqlite db 
                file at the specified path with the specified name and 
                once the db file is created prints 'New DB Created' and 
                returns 'DB created'


    SAMPLE USAGE
        build_dbs()
    '''
    if os.path.isfile(DB_PATH+DB_FILENAME):
        print( "DB Already Exsist")
        print(os.getcwd())
        return "DB Exsist"
    else:
        print ("Creating Database")
        """ create a database connection to a SQLite database """
        conn = None
        try:
            
            conn = sqlite3.connect(DB_PATH+DB_FILENAME)
            print("New DB Created")
        except Error as e:
            print(e)
            return "Error"
        finally:
            if conn:
                conn.close()
                return "DB Created"

###############################################################################
# Define function to load the csv file to the database
# ##############################################################################

def load_data_into_db(DB_PATH, DB_FILENAME, DATA_DIRECTORY, RAW_DATA_FILENAME, LOADED_DATA_TABLENAME):
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
    df_lead_scoring = pd.read_csv(DATA_DIRECTORY+RAW_DATA_FILENAME) #, index_col=[0])
    
    # replacing any null values present in 'toal_leads_dropped' and
    # 'referred_lead' with 0.
    df_lead_scoring["total_leads_dropped"] = df_lead_scoring["total_leads_dropped"].fillna(0)
    df_lead_scoring["referred_lead"] = df_lead_scoring["referred_lead"].fillna(0)
    
    # writing to the db
    df_lead_scoring.to_sql(name=LOADED_DATA_TABLENAME, con=conn, if_exists='replace', index=False)
    

###############################################################################
# Define function to map cities to their respective tiers
# ##############################################################################

    
def map_city_tier(DB_PATH, DB_FILENAME, city_tier_mapping, LOADED_DATA_TABLENAME, CITY_TIER_MAPPED_TABLENAME):
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
    df_lead_scoring = pd.read_sql('select * from ' + LOADED_DATA_TABLENAME, conn)
    
    # map city tier
    df_lead_scoring["city_tier"] = df_lead_scoring["city_mapped"].map(city_tier_mapping)
    df_lead_scoring["city_tier"] = df_lead_scoring["city_tier"].fillna(3.0)
    df_lead_scoring = df_lead_scoring.drop(['city_mapped'], axis = 1)
    
    # writing to the db
    df_lead_scoring.to_sql(name=CITY_TIER_MAPPED_TABLENAME, con=conn, if_exists='replace', index=False)

###############################################################################
# Define function to map insignificant categorial variables to "others"
# ##############################################################################


def map_categorical_vars(DB_PATH, DB_FILENAME, list_platform, list_medium, list_source, CITY_TIER_MAPPED_TABLENAME, CATEGORICAL_VARIABLES_MAPPED_TABLENAME):
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


##############################################################################
# Define function that maps interaction columns into 4 types of interactions
# #############################################################################
def interactions_mapping(DB_PATH, DB_FILENAME, CATEGORICAL_VARIABLES_MAPPED_TABLENAME, INDEX_COLUMNS, TARGET_COLUMN, INTERACTION_MAPPING_FILE, MODEL_INPUT_TABLENAME, SELECTED_FEATURES, INTERACTIONS_MAPPED_TABLENAME):
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
    
