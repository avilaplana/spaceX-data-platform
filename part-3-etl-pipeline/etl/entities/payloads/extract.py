import logging
import requests

logger = logging.getLogger(__name__)

def extract_payloads():
    """
    Extract payload data from the SpaceX API.
    
    Returns:
        list: Raw payload data from the API
    """
    logger.info("Extracting payload data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/payloads')
        response.raise_for_status()
        
        payloads = response.json()
        logger.info(f"Successfully extracted {len(payloads)} payloads")
        return payloads
        
    except Exception as e:
        logger.error(f"Error extracting payloads: {str(e)}")
        raise 