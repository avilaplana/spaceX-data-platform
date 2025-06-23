import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_landpads(conn, landpads):
    """
    Load transformed landpad data into the database.
    
    Args:
        conn: Database connection
        landpads (list): List of transformed landpad records
    """
    if not landpads:
        logger.warning("No landpads to load")
        return

    logger.info(f"Loading {len(landpads)} landpads into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_landpad CASCADE")
            
            # Insert new data
            columns = landpads[0].keys()
            query = f"""
                INSERT INTO dim_landpad ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in landpads]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded landpads")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading landpads: {str(e)}")
        raise 