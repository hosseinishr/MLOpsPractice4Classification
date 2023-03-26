# You can create more variables according to your project. The following are the basic variables that have been provided to you

ROOT_PATH = '/home/Assignment/airflow/dags/Lead_scoring_data_pipeline/'
DB_PATH = ROOT_PATH
DB_FILENAME = 'lead_scoring_data_cleaning.db'
DATA_DIRECTORY = ROOT_PATH + 'data/'
RAW_DATA_FILENAME = 'leadscoring.csv'
LOADED_DATA_TABLENAME = 'loaded_data'
CITY_TIER_MAPPED_TABLENAME = 'city_tier_mapped'
CATEGORICAL_VARIABLES_MAPPED_TABLENAME = 'categorical_variables_mapped'
TARGET_COLUMN = 'app_complete_flag'
INTERACTION_PATH = ROOT_PATH + 'mapping/'
INTERACTION_FILENAME = 'interaction_mapping.csv'
INTERACTION_MAPPING_FILE = INTERACTION_PATH + INTERACTION_FILENAME
INTERACTIONS_MAPPED_TABLENAME = 'interactions_mapped'
MODEL_INPUT_TABLENAME = 'model_input'
SELECTED_FEATURES = ['total_leads_dropped', 'city_tier', 'referred_lead', 'app_complete_flag', 
                     'first_platform_c', 'first_utm_medium_c', 'first_utm_source_c']
INDEX_COLUMNS = ['created_date', 'first_platform_c', 'first_utm_medium_c', 'first_utm_source_c', 
                 'total_leads_dropped', 'city_tier', 'referred_lead']
