import logging
import requests

logger = logging.getLogger(__name__)

def extract_cores():
    """
    Extract core data from the SpaceX API.
    
    Returns:
        list: Raw core data from the API
    """
    logger.info("Extracting core data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/cores')
        response.raise_for_status()
        
        cores = response.json()
        logger.info(f"Successfully extracted {len(cores)} cores")
        return cores
        
    except Exception as e:
        logger.error(f"Error extracting cores: {str(e)}")
        raise 