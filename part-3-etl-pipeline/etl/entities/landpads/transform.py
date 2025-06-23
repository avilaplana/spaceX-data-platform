import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def transform_landpads(landpads_data):
    """
    Transform raw landpads data into a format suitable for database loading.
    
    Args:
        landpads_data (list): Raw landpads data from the API
        
    Returns:
        list: Transformed landpad records
    """
    logger.info("Transforming landpads data...")
    
    landpads = []
    
    for landpad in landpads_data:
        if not landpad.get('id'):
            logger.warning("Skipping landpad without ID")
            continue
            
        landpads.append({
            'external_landpad_id': landpad['id'],
            'name': landpad.get('name'),
            'full_name': landpad.get('full_name'),
            'status': landpad.get('status'),
            'type': landpad.get('type'),
            'locality': landpad.get('locality'),
            'region': landpad.get('region'),
            'latitude': landpad.get('latitude'),
            'longitude': landpad.get('longitude'),
            'landing_attempts': landpad.get('landing_attempts'),
            'landing_successes': landpad.get('landing_successes'),
            'wikipedia': landpad.get('wikipedia'),
            'details': landpad.get('details')
        })
    
    logger.info(f"Transformed {len(landpads)} landpads")
    return landpads 