import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def transform_starlink(starlink_data):
    """
    Transform raw starlink data into a format suitable for database loading.
    
    Args:
        starlink_data (list): Raw starlink data from the API
        
    Returns:
        list: Transformed starlink records
    """
    logger.info("Transforming starlink data...")
    
    starlinks = []
    
    for satellite in starlink_data:
        if not satellite.get('id'):
            logger.warning("Skipping starlink satellite without ID")
            continue
            
        starlinks.append({
            'external_starlink_id': satellite['id'],
            'version': satellite.get('version'),
            'launch': satellite.get('launch'),
            'longitude': satellite.get('longitude'),
            'latitude': satellite.get('latitude'),
            'height_km': satellite.get('height_km'),
            'velocity_kms': satellite.get('velocity_kms')            
        })
    
    logger.info(f"Transformed {len(starlinks)} starlink satellites")
    return starlinks 