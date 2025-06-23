import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_cores(conn, cores):
    """
    Load transformed core data into the database.
    
    Args:
        conn: Database connection
        cores (list): List of transformed core records
    """
    if not cores:
        logger.warning("No cores to load")
        return

    logger.info(f"Loading {len(cores)} cores into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_core CASCADE")
            
            # Insert new data
            columns = cores[0].keys()
            query = f"""
                INSERT INTO dim_core ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in cores]
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded cores")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading cores: {str(e)}")
        raise 