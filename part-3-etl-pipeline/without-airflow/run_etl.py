#!/usr/bin/env python3

import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2

# Import all entity modules
from etl.entities.launchpads import extract_launchpads, transform_launchpads, load_launchpads
from etl.entities.cores import extract_cores, transform_cores, load_cores
from etl.entities.rockets import extract_rockets, transform_rockets, load_rockets
from etl.entities.payloads import extract_payloads, transform_payloads, load_payloads
from etl.entities.crew import extract_crew, transform_crew, load_crew
from etl.entities.ships import extract_ships, transform_ships, load_ships
from etl.entities.capsules import extract_capsules, transform_capsules, load_capsules
from etl.entities.landpads import extract_landpads, transform_landpads, load_landpads
from etl.entities.starlink import extract_starlink, transform_starlink, load_starlink
from etl.entities.roadster import extract_roadster, transform_roadster, load_roadster
from etl.entities.company import extract_company, transform_company, load_company
from etl.entities.launches import extract_launches, transform_launches, load_launches

# Load environment variables
load_dotenv()

# Configure logging
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_dir, f'etl_{timestamp}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def get_db_params():
    """Get database connection parameters from environment variables."""
    return {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT')
    }

def run_entity_etl(entity_name, extract_func, transform_func, load_func):
    """Run ETL process for a single entity."""
    try:
        logger.info(f"Starting ETL process for {entity_name}")
        
        # Extract
        logger.info(f"Extracting {entity_name} data...")
        raw_data = extract_func()
        logger.info(f"Extracted {len(raw_data) if raw_data else 0} {entity_name} records")
        
        # Transform
        logger.info(f"Transforming {entity_name} data...")
        
        # For launches, we need a database cursor for lookups
        if entity_name == 'launches':
            try:
                with psycopg2.connect(**get_db_params()) as conn:
                    with conn.cursor() as cursor:
                        transformed_data = transform_func(raw_data, cursor)
                logger.info(f"Transformed {entity_name} data with database lookups")
            except Exception as e:
                logger.error(f"Database error during {entity_name} transform: {str(e)}")
                raise
        else:
            # Dimension entities don't need database cursor
            transformed_data = transform_func(raw_data)
            logger.info(f"Transformed {entity_name} data")
        
        # Load
        logger.info(f"Loading {entity_name} data...")
        try:
            with psycopg2.connect(**get_db_params()) as conn:
                if entity_name == 'launches':
                    # Launches entity handles multiple data types
                    load_func(conn, *transformed_data)
                else:
                    # Dimension entities handle a single data type
                    load_func(conn, transformed_data)
            logger.info(f"Loaded {entity_name} data")
        except Exception as e:
            logger.error(f"Database error while loading {entity_name}: {str(e)}")
            raise
        
        logger.info(f"Completed ETL process for {entity_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error in {entity_name} ETL process: {str(e)}")
        return False

def main():
    """Main ETL process."""
    logger.info("Starting ETL process")
    
    # Define entities in order of processing (launches last due to dependencies)
    entities = [
        ('launchpads', extract_launchpads, transform_launchpads, load_launchpads),
        ('cores', extract_cores, transform_cores, load_cores),
        ('rockets', extract_rockets, transform_rockets, load_rockets),
        ('payloads', extract_payloads, transform_payloads, load_payloads),
        ('crew', extract_crew, transform_crew, load_crew),
        ('ships', extract_ships, transform_ships, load_ships),
        ('capsules', extract_capsules, transform_capsules, load_capsules),
        ('landpads', extract_landpads, transform_landpads, load_landpads),
        ('starlink', extract_starlink, transform_starlink, load_starlink),
        ('roadster', extract_roadster, transform_roadster, load_roadster),
        ('company', extract_company, transform_company, load_company),
        ('launches', extract_launches, transform_launches, load_launches)  # Process launches last
    ]
    
    # Track success and failures
    successful_entities = []
    failed_entities = []
    
    # Process each entity
    for entity_name, extract_func, transform_func, load_func in entities:
        if run_entity_etl(entity_name, extract_func, transform_func, load_func):
            successful_entities.append(entity_name)
        else:
            failed_entities.append(entity_name)
    
    # Log summary
    logger.info("ETL process completed")
    logger.info(f"Successfully processed entities: {', '.join(successful_entities)}")
    if failed_entities:
        logger.error(f"Failed to process entities: {', '.join(failed_entities)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 