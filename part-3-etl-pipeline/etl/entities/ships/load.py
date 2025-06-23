import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_ships(conn, ships):
    """
    Load transformed ship data into the database.
    
    Args:
        conn: Database connection
        ships (list): List of transformed ship records
    """
    if not ships:
        logger.warning("No ships to load")
        return

    logger.info(f"Loading {len(ships)} ships into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_ship CASCADE")
            
            # Insert new data
            columns = ships[0].keys()
            query = f"""
                INSERT INTO dim_ship ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[record[col] for col in columns] for record in ships]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded ships")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading ships: {str(e)}")
        raise 