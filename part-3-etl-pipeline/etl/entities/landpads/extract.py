import logging
import requests

logger = logging.getLogger(__name__)

def extract_landpads():
    """
    Extract landpads data from the SpaceX API.
    
    Returns:
        list: Raw landpads data from the API
    """
    logger.info("Extracting landpads data from SpaceX API...")
    
    try:
        response = requests.get('https://api.spacexdata.com/v4/landpads')
        response.raise_for_status()
        
        landpads = response.json()
        logger.info(f"Successfully extracted {len(landpads)} landpads")
        return landpads
        
    except Exception as e:
        logger.error(f"Error extracting landpads: {str(e)}")
        raise 