import logging
import requests

logger = logging.getLogger(__name__)

def extract_starlink():
    """
    Extract starlink data from the SpaceX API.
    
    Returns:
        list: Raw starlink data from the API
    """
    logger.info("Extracting starlink data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/starlink')
        response.raise_for_status()
        
        starlinks = response.json()
        logger.info(f"Successfully extracted {len(starlinks)} starlink satellites")
        return starlinks
        
    except Exception as e:
        logger.error(f"Error extracting starlink data: {str(e)}")
        raise 