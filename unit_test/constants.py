# You can create more variables according to your project. The following are the basic variables that have been provided to you

ROOT_PATH = '/home/Assignment/data_pipeline/unit_test/'
DB_PATH = ROOT_PATH # + 'scripts/'
DB_FILENAME = 'unit_test_output.db'
DATA_DIRECTORY = ROOT_PATH #+ 'data/'
RAW_DATA_FILENAME = 'leadscoring_test.csv'
LOADED_DATA_TABLENAME = 'loaded_data'
CITY_TIER_MAPPED_TABLENAME = 'city_tier_mapped'
CATEGORICAL_VARIABLES_MAPPED_TABLENAME = 'categorical_variables_mapped'
TARGET_COLUMN = 'app_complete_flag'
INTERACTION_PATH = DB_PATH # + 'mapping/'
INTERACTION_FILENAME = 'interaction_mapping.csv'
INTERACTION_MAPPING_FILE = INTERACTION_PATH + INTERACTION_FILENAME
INTERACTIONS_MAPPED_TABLENAME = 'interactions_mapped'
MODEL_INPUT_TABLENAME = 'model_input'
SELECTED_FEATURES = ['total_leads_dropped', 'city_tier', 'referred_lead', 'app_complete_flag', 
                     'first_platform_c', 'first_utm_medium_c', 'first_utm_source_c']
INDEX_COLUMNS = ['created_date', 'first_platform_c', 'first_utm_medium_c', 'first_utm_source_c', 
                 'total_leads_dropped', 'city_tier', 'referred_lead']

DB_REFERENCE_FILENAME = 'unit_test_cases.db'
LOADED_DATA_TABLENAME_REFERENCE = 'loaded_data_test_case'
CITY_TIER_MAPPED_TABLENAME_REFERENCE = 'city_tier_mapped_test_case'
CATEGORICAL_VARIABLES_MAPPED_TABLENAME_REFERENCE = 'categorical_variables_mapped_test_case'
INTERACTIONS_MAPPED_TABLENAME_REFERENCE = 'interactions_mapped_test_case'