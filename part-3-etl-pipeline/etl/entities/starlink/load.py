import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_starlink(conn, starlinks):
    """
    Load transformed starlink data into the database.
    
    Args:
        conn: Database connection
        starlinks (list): List of transformed starlink records
    """
    if not starlinks:
        logger.warning("No starlinks to load")
        return

    logger.info(f"Loading {len(starlinks)} starlinks into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_starlink CASCADE")
            
            # Insert new data
            columns = starlinks[0].keys()
            query = f"""
                INSERT INTO dim_starlink ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in starlinks]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded starlinks")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading starlinks: {str(e)}")
        raise 