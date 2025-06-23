import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_capsules(conn, capsules):
    """
    Load transformed capsule data into the database.
    
    Args:
        conn: Database connection
        capsules (list): List of transformed capsule records
    """
    if not capsules:
        logger.warning("No capsules to load")
        return

    logger.info(f"Loading {len(capsules)} capsules into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_capsule CASCADE")
            
            # Insert new data
            columns = capsules[0].keys()
            query = f"""
                INSERT INTO dim_capsule ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in capsules]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded capsules")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading capsules: {str(e)}")
        raise 