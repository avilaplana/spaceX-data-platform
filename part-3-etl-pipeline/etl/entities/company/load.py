import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_company(conn, company):
    """
    Load transformed company data into the database.
    
    Args:
        conn: Database connection
        company (dict): Transformed company record
    """
    if not company:
        logger.warning("No company data to load")
        return

    logger.info("Loading company data into database")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute("TRUNCATE TABLE dim_company CASCADE")
            
            # Insert new data
            columns = company.keys()
            query = f"""
                INSERT INTO dim_company ({', '.join(columns)})
                VALUES %s
            """
            
            values = [[company[col] for col in columns]]            
            execute_values(cur, query, values)
            
            conn.commit()
            logger.info("Successfully loaded company data")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading company data: {str(e)}")
        raise 