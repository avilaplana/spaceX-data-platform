import logging
import requests

logger = logging.getLogger(__name__)

def extract_roadster():
    """
    Extract roadster data from the SpaceX API.
    
    Returns:
        dict: Raw roadster data from the API
    """
    logger.info("Extracting roadster data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/roadster')
        response.raise_for_status()
        
        roadster = response.json()
        logger.info("Successfully extracted roadster data")
        return roadster
        
    except Exception as e:
        logger.error(f"Error extracting roadster data: {str(e)}")
        raise 