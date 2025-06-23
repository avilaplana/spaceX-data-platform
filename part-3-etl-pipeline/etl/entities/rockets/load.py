import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_rockets(conn, rockets):
    """
    Load transformed rocket data into the database.
    
    Args:
        conn: Database connection
        rockets (list): List of transformed rocket records
    """
    if not rockets:
        logger.warning("No rockets to load")
        return

    logger.info(f"Loading {len(rockets)} rockets into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_rocket CASCADE")
            
            # Insert new data
            columns = rockets[0].keys()
            query = f"""
                INSERT INTO dim_rocket ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in rockets]
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded rockets")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading rockets: {str(e)}")
        raise 