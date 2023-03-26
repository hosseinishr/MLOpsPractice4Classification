# MLOps Implementation for Junk Leads Classification

## Table of Contents
* [Problem Statement](#problem-statement)
* [Workflow Explanation](#workflow-explanation)
* [Data Pipeline](#data-pipeline)
* [Training Pipeline](#training-pipeline)
* [Inference Pipeline](#inference-pipeline)
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



## Acknowledgements
- I would like to acknowledge the feedback, support and dataset provision by [upGrad](https://www.upgrad.com/gb) and The [International Institute of Information Technology (IIIT), Bangalore](https://www.iiitb.ac.in/).  
- Also, I would like to express my gratitude to [Gerzson Boros](https://www.linkedin.com/in/gerzson-boros/) for providing clarification and guidance to carry out this project. 
