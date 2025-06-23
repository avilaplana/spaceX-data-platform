from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def transform_launchpads(data):
    """
    Transform launchpad data from the SpaceX API into our database format.
    
    Args:
        data (dict): Raw launchpad data from the API
        
    Returns:
        list: List of transformed launchpad records
    """
    logger.info("Starting transformation of launchpad data...")
    
    launchpads = []
    for launchpad in data:
        launchpad_id = launchpad.get('id')
        if not launchpad_id:
            continue
            
        launchpads.append({
            'external_site_id': launchpad_id,
            'name': launchpad.get('name'),
            'full_name': launchpad.get('full_name'),
            'status': launchpad.get('status'),
            'locality': launchpad.get('locality'),
            'region': launchpad.get('region'),
            'latitude': launchpad.get('latitude'),
            'longitude': launchpad.get('longitude'),
            'launch_attempts': launchpad.get('launch_attempts'),
            'launch_successes': launchpad.get('launch_successes')
        })
    
    logger.info(f"Transformed {len(launchpads)} launchpads")
    return launchpads 