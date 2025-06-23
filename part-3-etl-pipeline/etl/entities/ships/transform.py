import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def transform_ships(ships_data):
    """
    Transform raw ships data into a format suitable for database loading.
    
    Args:
        ships_data (list): Raw ships data from the API
        
    Returns:
        list: Transformed ship records
    """
    logger.info("Transforming ships data...")
    
    ships = []
    
    for ship in ships_data:
        if not ship.get('id'):
            logger.warning("Skipping ship without ID")
            continue
            
        ships.append({
            'external_ship_id': ship['id'],
            'name': ship.get('name'),
            'type': ship.get('type'),
            'active': ship.get('active'),
            'imo': ship.get('imo'),
            'mmsi': ship.get('mmsi'),
            'abs': ship.get('abs'),
            'class': ship.get('class'),
            'mass_kg': ship.get('mass_kg'),
            'mass_lbs': ship.get('mass_lbs'),
            'year_built': ship.get('year_built'),
            'home_port': ship.get('home_port'),
            'status': ship.get('status'),
            'speed_kn': ship.get('speed_kn'),
            'course_deg': ship.get('course_deg'),
            'latitude': ship.get('latitude'),
            'longitude': ship.get('longitude'),
            'last_ais_update': ship.get('last_ais_update'),
            'link': ship.get('link'),
            'image': ship.get('image')
        })
    
    logger.info(f"Transformed {len(ships)} ships")
    return ships 