import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_launchpads(conn, launchpads):
    """
    Load transformed launchpad data into the database.
    
    Args:
        conn: Database connection
        launchpads (list): List of transformed launchpad records
    """
    if not launchpads:
        logger.warning("No launchpads to load")
        return

    logger.info(f"Loading {len(launchpads)} launchpads into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_launch_site CASCADE")
            
            # Insert new data
            columns = launchpads[0].keys()
            query = f"""
                INSERT INTO dim_launch_site ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in launchpads]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded launchpads")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading launchpads: {str(e)}")
        raise 