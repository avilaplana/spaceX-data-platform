import logging
import requests

logger = logging.getLogger(__name__)

def extract_ships():
    """
    Extract ships data from the SpaceX API.
    
    Returns:
        list: Raw ships data from the API
    """
    logger.info("Extracting ships data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/ships')
        response.raise_for_status()
        
        ships = response.json()
        logger.info(f"Successfully extracted {len(ships)} ships")
        return ships
        
    except Exception as e:
        logger.error(f"Error extracting ships: {str(e)}")
        raise 