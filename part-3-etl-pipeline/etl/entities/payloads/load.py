import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_payloads(conn, payloads):
    """
    Load transformed payload data into the database.
    
    Args:
        conn: Database connection
        payloads (list): List of transformed payload records
    """
    if not payloads:
        logger.warning("No payloads to load")
        return

    logger.info(f"Loading {len(payloads)} payloads into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_payload CASCADE")
            
            # Insert new data
            columns = payloads[0].keys()
            query = f"""
                INSERT INTO dim_payload ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in payloads]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded payloads")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading payloads: {str(e)}")
        raise 