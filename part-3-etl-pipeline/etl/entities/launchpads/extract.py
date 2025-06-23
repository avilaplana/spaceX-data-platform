import logging
import requests

logger = logging.getLogger(__name__)

def extract_launchpads():
    """
    Extract launchpad data from the SpaceX API.
    
    Returns:
        list: Raw launchpad data from the API
    """
    logger.info("Extracting launchpad data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/launchpads')
        response.raise_for_status()
        
        launchpads = response.json()
        logger.info(f"Successfully extracted {len(launchpads)} launchpads")
        return launchpads
        
    except Exception as e:
        logger.error(f"Error extracting launchpads: {str(e)}")
        raise 