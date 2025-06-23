from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import sys
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Add the ETL package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../etl')))

# Import all dimension table ETL functions
from etl.entities.company.extract import extract_company
from etl.entities.company.transform import transform_company
from etl.entities.company.load import load_company

from etl.entities.launchpads.extract import extract_launchpads
from etl.entities.launchpads.transform import transform_launchpads
from etl.entities.launchpads.load import load_launchpads

from etl.entities.rockets.extract import extract_rockets
from etl.entities.rockets.transform import transform_rockets
from etl.entities.rockets.load import load_rockets

from etl.entities.roadster.extract import extract_roadster
from etl.entities.roadster.transform import transform_roadster
from etl.entities.roadster.load import load_roadster

from etl.entities.ships.extract import extract_ships
from etl.entities.ships.transform import transform_ships
from etl.entities.ships.load import load_ships

from etl.entities.capsules.extract import extract_capsules
from etl.entities.capsules.transform import transform_capsules
from etl.entities.capsules.load import load_capsules

from etl.entities.cores.extract import extract_cores
from etl.entities.cores.transform import transform_cores
from etl.entities.cores.load import load_cores

from etl.entities.crew.extract import extract_crew
from etl.entities.crew.transform import transform_crew
from etl.entities.crew.load import load_crew

from etl.entities.landpads.extract import extract_landpads
from etl.entities.landpads.transform import transform_landpads
from etl.entities.landpads.load import load_landpads

from etl.entities.payloads.extract import extract_payloads
from etl.entities.payloads.transform import transform_payloads
from etl.entities.payloads.load import load_payloads

from etl.entities.starlink.extract import extract_starlink
from etl.entities.starlink.transform import transform_starlink
from etl.entities.starlink.load import load_starlink

# Import fact table ETL functions
from etl.entities.launches.extract import extract_launches
from etl.entities.launches.transform import transform_launches
from etl.entities.launches.load import load_launches

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_db_connection():
    """Create a database connection"""
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'spacex_data'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres')
    )

# Dimension table ETL functions
def run_sites_etl():
    """Run ETL for rockets data"""
    data = extract_launchpads()
    transformed_data = transform_launchpads(data)
    conn = get_db_connection()
    try:
        load_launchpads(conn, transformed_data)
    finally:
        conn.close()

def run_rockets_etl():
    """Run ETL for rockets data"""
    data = extract_rockets()
    transformed_data = transform_rockets(data)
    conn = get_db_connection()
    try:
        load_rockets(conn, transformed_data)
    finally:
        conn.close()

def run_company_etl():
    """Run ETL for company data"""
    data = extract_company()
    transformed_data = transform_company(data)
    conn = get_db_connection()
    try:
        load_company(conn, transformed_data)
    finally:
        conn.close()

def run_roadster_etl():
    """Run ETL for roadster data"""
    data = extract_roadster()
    transformed_data = transform_roadster(data)
    conn = get_db_connection()
    try:
        load_roadster(conn, transformed_data)
    finally:
        conn.close()

def run_ships_etl():
    """Run ETL for ships data"""
    data = extract_ships()
    transformed_data = transform_ships(data)
    conn = get_db_connection()
    try:
        load_ships(conn, transformed_data)
    finally:
        conn.close()

def run_capsules_etl():
    """Run ETL for capsules data"""
    data = extract_capsules()
    transformed_data = transform_capsules(data)
    conn = get_db_connection()
    try:
        load_capsules(conn, transformed_data)
    finally:
        conn.close()

def run_cores_etl():
    """Run ETL for cores data"""
    data = extract_cores()
    transformed_data = transform_cores(data)
    conn = get_db_connection()
    try:
        load_cores(conn, transformed_data)
    finally:
        conn.close()

def run_crew_etl():
    """Run ETL for crew data"""
    data = extract_crew()
    transformed_data = transform_crew(data)
    conn = get_db_connection()
    try:
        load_crew(conn, transformed_data)
    finally:
        conn.close()

def run_landpads_etl():
    """Run ETL for landpads data"""
    data = extract_landpads()
    transformed_data = transform_landpads(data)
    conn = get_db_connection()
    try:
        load_landpads(conn, transformed_data)
    finally:
        conn.close()

def run_payloads_etl():
    """Run ETL for payloads data"""
    data = extract_payloads()
    transformed_data = transform_payloads(data)
    conn = get_db_connection()
    try:
        load_payloads(conn, transformed_data)
    finally:
        conn.close()

def run_starlink_etl():
    """Run ETL for starlink data"""
    data = extract_starlink()
    transformed_data = transform_starlink(data)
    conn = get_db_connection()
    try:
        load_starlink(conn, transformed_data)
    finally:
        conn.close()

# Fact table ETL function
def run_launches_etl():
    """Run ETL for launches data"""
    data = extract_launches()
    transformed_data = transform_launches(data)
    conn = get_db_connection()
    try:
        load_launches(conn, *transformed_data)
    finally:
        conn.close()

with DAG(
    'spacex_etl',
    default_args=default_args,
    description='ETL process for SpaceX data',
    schedule_interval=None,
    catchup=False,
    tags=['spacex', 'etl'],
) as dag:

    # Dimension tables first
    company_task = PythonOperator(
        task_id='sites_etl',
        python_callable=run_sites_etl,
    )

    company_task = PythonOperator(
        task_id='rockets_etl',
        python_callable=run_rockets_etl,
    )

    company_task = PythonOperator(
        task_id='company_etl',
        python_callable=run_company_etl,
    )

    roadster_task = PythonOperator(
        task_id='roadster_etl',
        python_callable=run_roadster_etl,
    )

    ships_task = PythonOperator(
        task_id='ships_etl',
        python_callable=run_ships_etl,
    )

    capsules_task = PythonOperator(
        task_id='capsules_etl',
        python_callable=run_capsules_etl,
    )

    cores_task = PythonOperator(
        task_id='cores_etl',
        python_callable=run_cores_etl,
    )

    crew_task = PythonOperator(
        task_id='crew_etl',
        python_callable=run_crew_etl,
    )

    landpads_task = PythonOperator(
        task_id='landpads_etl',
        python_callable=run_landpads_etl,
    )

    payloads_task = PythonOperator(
        task_id='payloads_etl',
        python_callable=run_payloads_etl,
    )

    starlink_task = PythonOperator(
        task_id='starlink_etl',
        python_callable=run_starlink_etl,
    )

    # Fact table last
    launches_task = PythonOperator(
        task_id='launches_etl',
        python_callable=run_launches_etl,
    )

    # Set task dependencies - all dimensions must complete before launches
    [
        company_task,
        roadster_task,
        ships_task,
        capsules_task,
        cores_task,
        crew_task,
        landpads_task,
        payloads_task,
        starlink_task
    ] >> launches_task 