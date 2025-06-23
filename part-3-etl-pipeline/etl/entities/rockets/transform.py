from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def transform_rockets(data):
    """
    Transform rocket data from the SpaceX API into our database format.
    
    Args:
        data (list): Raw rocket data from the API
        
    Returns:
        list: List of transformed rocket records
    """
    logger.info("Starting transformation of rocket data...")
    
    rockets = []
    for rocket in data:
        rocket_id = rocket.get('id')
        if not rocket_id:
            continue
            
        rockets.append({
            'external_rocket_id': rocket_id,
            'name': rocket.get('name'),
            'type': rocket.get('type'),
            'active': rocket.get('active'),
            'stages': rocket.get('stages'),
            'boosters': rocket.get('boosters'),
            'cost_per_launch': rocket.get('cost_per_launch'),
            'success_rate_pct': rocket.get('success_rate_pct'),
            'first_flight': rocket.get('first_flight'),
            'country': rocket.get('country'),
            'company': rocket.get('company'),            
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })
    
    logger.info(f"Transformed {len(rockets)} rockets")
    return rockets 