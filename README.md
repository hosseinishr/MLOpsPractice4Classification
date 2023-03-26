# MLOps Implementation for Junk Leads Classification

## Table of Contents
* [Problem Statement](#problem-statement)
* [Workflow Explanation](#workflow-explanation)
* [Model Experimentation in mlflow](#model-experimentation-in-mlflow)
* [Data Pipeline in Airflow](#data-pipeline-in-airflow)
* [Training Pipeline in Airflow](#training-pipeline-in-airflow)
* [Inference Pipeline in Airflow](#inference-pipeline-in-airflow)
* [Acknowledgements](#acknowledgements)

## Problem Statement
An education platform wants to classify the junk leads from genuine ones in order to increase revenue by investing more (time, and support) on the genuine leads to turn them into customers. 'Lead' in this context means the visitors of their digital platforms (website, application, etc.) that might become their potential customers, meaning the leads might fill the application form, pay the fees, and start to use their platform. In this way, the revenue of the education platform will increase if more time and support is offered to the genuine leads to turn them into customers/users of the platform.  
  
The intention of this exercise is to automate the process of classification of junk leads via implementing data pipeline, training pipeline and inference pipeline. The objective is to classify the junk leads so that the education platform could spend more time and offer more support to the genuine leads, who with more support, clarifications and more interactions with them they might turn into customers (users) of the platform.

## Workflow Explanation
The dataset provided, in brief, has data of 240,000 leads with the features on: lead's city, digital platform, source and medium through which the lead has landed on the education platform, dozens types of lead's interaction with the platform, and eventually a flag, which identifies whether or not the lead has filled the application form.  

The following steps have been performed in order to prepare the data for the data, training and inference pipelines:  
- Pandas profiling were used to obtain a feel of the dataset
- For the following features, in order to reduce the number of categories, the features with value counts more than 90% were kept, and the rest were grouped into a category called 'others': lead's city, digital platform, source and medium through which the lead has landed on the education platform.
- For the dozens types of lead's interaction with the platform, all these were grouped into Assistance Interaction, Career Interaction, Payment Interaction, and Syllabus Interaction.  

Regarding model experimentation and pipeline automation, the following have been utilised:
- mlflow were used to keep track of models' version and if a model coule go to the Staging, Production, or Archive levels.
- airflow were used for automation of data, training, and inference pipelines.

## Model Experimentation in mlflow
The screenshots below demonstrate how the experiments were logged in mlflow, artifacts of the model, and a version of the model being promoted to Production level.

<img src="/images/mlflow_all_experiments.png" width = 1000>  
  
<img src="/images/mlflow_best_model_artifacts.png" width = 1000>  
  
<img src="/images/mlflow_exp_artifact_LightGBM.png" width = 1000>  
  
<img src="/images/mlflow_LightGBM_production_stage.png" width = 1000>  
  
## Data Pipeline in Airflow
The data pipeline consists of the following tasks/DAGs:
- building databases (db) via sqlite3, so that all the tasks read data from db, and write their output to the db.
- checking the schema of the raw data to ensure/avoid any data drift.
- loading data from csv file into db.
- mapping all the cities into few major categories.
- mapping the digital platform, source and medium through which the lead has landed on the education platform, into few categoiries.
- mapping all the dozens types of lead's interaction with the platform, all these were grouped into Assistance Interaction, Career Interaction, Payment Interaction, and Syllabus Interaction.
- checking the schema of the final dataset to be suitable to be fed into training pipeline for ML models.
  
The pictures below, show the successful implementation of the data pipeline in airflow, and the relation of different DAGs in this pipeline.
<img src="/images/airflow_execution_data_ppln.png" width = 1000>  
  
<img src="/images/airflow_graph_data_ppln.png" width = 1000>  

In this stage, unit test functions have also been developed to ensure all the above functions produce the expected output results.
  
## Training Pipeline in Airflow
The training pipeline consists of the following tasks/DAGs:
- one hot encoding all the categorical variables.
- training LightGBM model.
  
The pictures below, show the successful implementation of the training pipeline in airflow, and the relation of different DAGs in this pipeline.
<img src="/images/airflow_execution_training_ppln.png" width = 1000>  
  
<img src="/images/airflow_graph_training_ppln.png" width = 1000>

## Inference Pipeline in Airflow
The inference pipeline consists of few of the DAGs/tasks in the data pipeline (since new data should first go though some cleaning/unifying process) and in inference specific DAGs/tasks as follows:
- loading data from csv file into db.
- mapping all the cities into few major categories.
- mapping the digital platform, source and medium through which the lead has landed on the education platform, into few categoiries.
- mapping all the dozens types of lead's interaction with the platform, all these were grouped into Assistance Interaction, Career Interaction, Payment Interaction, and Syllabus Interaction.
- one hot encoding all the categorical variables.
- checking the schema of the final dataset to be suitable to be fed into training pipeline for LightGBM model.
- prediction on the new dataset.
- calculation of the percentages of 1's and 0's in the prediction and writing to a text file.

The pictures below, show the successful implementation of the training pipeline in airflow, and the relation of different DAGs in this pipeline.
<img src="/images/airflow_execution_inference_ppln.png" width = 1000>  
  
<img src="/images/airflow_graph_inference_ppln.png" width = 1000>


## Acknowledgements
- I would like to acknowledge the feedback, support and dataset provision by [upGrad](https://www.upgrad.com/gb) and The [International Institute of Information Technology (IIIT), Bangalore](https://www.iiitb.ac.in/).  
- Also, I would like to express my gratitude to [Gerzson Boros](https://www.linkedin.com/in/gerzson-boros/) for providing clarification and guidance to carry out this project. 
