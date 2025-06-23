import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_crew(conn, crew):
    """
    Load transformed crew data into the database.
    
    Args:
        conn: Database connection
        crew (list): List of transformed crew records
    """
    if not crew:
        logger.warning("No crew to load")
        return

    logger.info(f"Loading {len(crew)} crew members into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_crew CASCADE")
            
            # Insert new data
            columns = crew[0].keys()
            query = f"""
                INSERT INTO dim_crew ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in crew]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded crew")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading crew: {str(e)}")
        raise 