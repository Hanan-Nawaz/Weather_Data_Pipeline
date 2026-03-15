"""
DAG: weather_data_pipeline

Description:
This DAG runs the ETL pipeline for collecting, transforming, and loading weather data
into a database. It orchestrates the following steps:

1. Extract weather data from API
2. Transform and clean the data
3. Load processed data into PostgreSQL

Schedule: Hourly
Owner: airflow
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2026, 3, 13),
}

# DAG definition
with DAG(
    'weather_data_pipeline',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
    doc_md="""
    # Weather Data ETL Pipeline
    This DAG runs every hour to fetch weather data from the API, transform it,
    and load it into a PostgreSQL database.
    """
) as dag:

    # Task: Run the ETL pipeline
    etl = BashOperator(
        task_id='etl_pipeline',
        bash_command='cd /Users/hanan-nawaz/Documents/Projects/weather_data_pipeline && python main.py',
        doc_md="""
        ## ETL Pipeline Task
        Executes the main ETL Python script:
        1. Extract data from API
        2. Transform the data (normalize, rename, clean)
        3. Load the data into PostgreSQL
        """
    )

    # Single task DAG: no dependencies to set