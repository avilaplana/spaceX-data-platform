import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def transform_roadster(roadster_data):
    """
    Transform raw roadster data into a format suitable for database loading.
    
    Args:
        roadster_data (dict): Raw roadster data from the API
        
    Returns:
        dict: Transformed roadster record
    """
    logger.info("Transforming roadster data...")
    
    if not roadster_data.get('id'):
        logger.error("Roadster data missing ID")
        raise ValueError("Roadster data must contain an ID")
    
    roadster = {
        'external_roadster_id': roadster_data['id'],
        'name': roadster_data.get('name'),
        'launch_date_utc': roadster_data.get('launch_date_utc'),
        'launch_date_unix': roadster_data.get('launch_date_unix'),
        'launch_mass_kg': roadster_data.get('launch_mass_kg'),
        'launch_mass_lbs': roadster_data.get('launch_mass_lbs'),
        'norad_id': roadster_data.get('norad_id'),
        'epoch_jd': roadster_data.get('epoch_jd'),
        'orbit_type': roadster_data.get('orbit_type'),
        'apoapsis_au': roadster_data.get('apoapsis_au'),
        'periapsis_au': roadster_data.get('periapsis_au'),
        'semi_major_axis_au': roadster_data.get('semi_major_axis_au'),
        'eccentricity': roadster_data.get('eccentricity'),
        'inclination': roadster_data.get('inclination'),
        'longitude': roadster_data.get('longitude'),
        'periapsis_arg': roadster_data.get('periapsis_arg'),
        'period_days': roadster_data.get('period_days'),
        'speed_kph': roadster_data.get('speed_kph'),
        'speed_mph': roadster_data.get('speed_mph'),
        'earth_distance_km': roadster_data.get('earth_distance_km'),
        'earth_distance_mi': roadster_data.get('earth_distance_mi'),
        'mars_distance_km': roadster_data.get('mars_distance_km'),
        'mars_distance_mi': roadster_data.get('mars_distance_mi'),
        'flickr_images': roadster_data.get('flickr_images', []),
        'wikipedia': roadster_data.get('wikipedia'),
        'video': roadster_data.get('video'),
        'details': roadster_data.get('details')
    }
    
    logger.info("Roadster data transformed successfully")
    return roadster 