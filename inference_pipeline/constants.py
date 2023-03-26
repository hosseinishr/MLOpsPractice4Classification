# You can create more variables according to your project. The following are the basic variables that have been provided to you

ROOT_PATH = '/home/Assignment/airflow/dags/Lead_scoring_inference_pipeline/'
DB_PATH = ROOT_PATH
DB_FILENAME = 'lead_scoring_data_cleaning.db'
DATA_DIRECTORY = ROOT_PATH + 'data/'
INFERENCE_DATA_FILENAME = 'leadscoring_inference.csv'
LOADED_DATA_TABLENAME = 'loaded_data'
CITY_TIER_MAPPED_TABLENAME = 'city_tier_mapped'
CATEGORICAL_VARIABLES_MAPPED_TABLENAME = 'categorical_variables_mapped'
TARGET_COLUMN = 'app_complete_flag'
INTERACTION_PATH = ROOT_PATH + 'mapping/'
INTERACTION_FILENAME = 'interaction_mapping.csv'
INTERACTION_MAPPING_FILE = INTERACTION_PATH + INTERACTION_FILENAME
PRED_DIST_FILE_PATH = ROOT_PATH + 'prediction_distribution.txt'
INTERACTIONS_MAPPED_TABLENAME = 'interactions_mapped'
MODEL_INPUT_TABLENAME = 'model_input'
SELECTED_FEATURES = ['total_leads_dropped', 'city_tier', 'referred_lead', 'app_complete_flag', 
                     'first_platform_c', 'first_utm_medium_c', 'first_utm_source_c']
INDEX_COLUMNS = ['created_date', 'first_platform_c', 'first_utm_medium_c', 'first_utm_source_c', 
                 'total_leads_dropped', 'city_tier', 'referred_lead']
USELESS_COLUMN = ['Unnamed: 0']

DF_FEATURES_INF_TABLENAME = 'df_features'
DF_PRED_TABLENAME = 'predictions'

DB_FILE_MLFLOW = 'Lead_scoring_mlflow_production.db'

# list of the features that needs to be there in the final encoded dataframe
ONE_HOT_ENCODED_FEATURES = ['total_leads_dropped', 'referred_lead',
                            'city_tier_1.0', 'city_tier_2.0', 'city_tier_3.0',
                            'first_platform_c_Level0', 'first_platform_c_Level3',
                            'first_platform_c_Level7', 'first_platform_c_Level1',
                            'first_platform_c_Level2', 'first_platform_c_Level8',
                            'first_platform_c_others', 'first_utm_medium_c_Level0',
                            'first_utm_medium_c_Level2', 'first_utm_medium_c_Level6',
                            'first_utm_medium_c_Level3', 'first_utm_medium_c_Level4',
                            'first_utm_medium_c_Level9', 'first_utm_medium_c_Level11',
                            'first_utm_medium_c_Level5', 'first_utm_medium_c_Level8',
                            'first_utm_medium_c_Level20', 'first_utm_medium_c_Level13',
                            'first_utm_medium_c_Level30', 'first_utm_medium_c_Level33',
                            'first_utm_medium_c_Level16', 'first_utm_medium_c_Level10',
                            'first_utm_medium_c_Level15', 'first_utm_medium_c_Level26',
                            'first_utm_medium_c_Level43', 'first_utm_medium_c_others',
                            'first_utm_source_c_Level2', 'first_utm_source_c_Level0',
                            'first_utm_source_c_Level7', 'first_utm_source_c_Level4',
                            'first_utm_source_c_Level6', 'first_utm_source_c_Level16',
                            'first_utm_source_c_Level5', 'first_utm_source_c_Level14',
                            'first_utm_source_c_others']

# list of features that need to be one-hot encoded
FEATURES_TO_ENCODE = ['city_tier', 'first_platform_c',
                      'first_utm_medium_c', 'first_utm_source_c']

TRACKING_URI = "http://0.0.0.0:6006"
MODEL_NAME = "LightGBM"
STAGE = "Production"


#DB_PATH = 
#DB_FILE_NAME = 

#DB_FILE_MLFLOW = 

#FILE_PATH = 

#TRACKING_URI = 

# experiment, model name and stage to load the model from mlflow model registry
#MODEL_NAME = 
#STAGE = 
#EXPERIMENT = 

# list of the features that needs to be there in the final encoded dataframe
#ONE_HOT_ENCODED_FEATURES = 

# list of features that need to be one-hot encoded
#FEATURES_TO_ENCODE = 
