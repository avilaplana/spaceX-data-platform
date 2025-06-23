import logging
import requests

logger = logging.getLogger(__name__)

def extract_company():
    """
    Extract company data from the SpaceX API.
    
    Returns:
        dict: Raw company data from the API
    """
    logger.info("Extracting company data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/company')
        response.raise_for_status()
        
        company = response.json()
        logger.info("Successfully extracted company data")
        return company
        
    except Exception as e:
        logger.error(f"Error extracting company data: {str(e)}")
        raise 