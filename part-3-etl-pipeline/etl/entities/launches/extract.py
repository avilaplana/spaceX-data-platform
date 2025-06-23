import logging
import requests

logger = logging.getLogger(__name__)

def extract_launches():
    """
    Extract launch data from the SpaceX API.
    
    Returns:
        list: Raw launch data from the API
    """
    logger.info("Extracting launch data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/launches')
        response.raise_for_status()
        
        launches = response.json()
        logger.info(f"Successfully extracted {len(launches)} launches")
        return launches
        
    except Exception as e:
        logger.error(f"Error extracting launches: {str(e)}")
        raise 