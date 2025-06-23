import logging
import requests

logger = logging.getLogger(__name__)

def extract_capsules():
    """
    Extract capsules data from the SpaceX API.
    
    Returns:
        list: Raw capsules data from the API
    """
    logger.info("Extracting capsules data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/capsules')
        response.raise_for_status()
        
        capsules = response.json()
        logger.info(f"Successfully extracted {len(capsules)} capsules")
        return capsules
        
    except Exception as e:
        logger.error(f"Error extracting capsules: {str(e)}")
        raise 