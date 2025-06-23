import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_roadster(conn, roadster):
    """
    Load transformed roadster data into the database.
    
    Args:
        conn: Database connection
        roadster (dict): Transformed roadster record
    """
    if not roadster:
        logger.warning("No roadster data to load")
        return

    logger.info("Loading roadster data into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_roadster CASCADE")
            
            # Insert new data
            columns = roadster.keys()
            query = f"""
                INSERT INTO dim_roadster ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[roadster[col] for col in columns]]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded roadster data")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading roadster data: {str(e)}")
        raise 