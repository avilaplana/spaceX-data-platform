import logging
import requests

logger = logging.getLogger(__name__)

def extract_rockets():
    """
    Extract rocket data from the SpaceX API.
    
    Returns:
        list: Raw rocket data from the API
    """
    logger.info("Extracting rocket data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/rockets')
        response.raise_for_status()
        
        rockets = response.json()
        logger.info(f"Successfully extracted {len(rockets)} rockets")
        return rockets
        
    except Exception as e:
        logger.error(f"Error extracting rockets: {str(e)}")
        raise 