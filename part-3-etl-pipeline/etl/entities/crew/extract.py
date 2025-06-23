import logging
import requests

logger = logging.getLogger(__name__)

def extract_crew():
    """
    Extract crew data from the SpaceX API.
    
    Returns:
        list: Raw crew data from the API
    """
    logger.info("Extracting crew data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/crew')
        response.raise_for_status()
        
        crew = response.json()
        logger.info(f"Successfully extracted {len(crew)} crew members")
        return crew
        
    except Exception as e:
        logger.error(f"Error extracting crew: {str(e)}")
        raise 