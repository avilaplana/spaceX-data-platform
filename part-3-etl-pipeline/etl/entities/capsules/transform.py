import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def transform_capsules(capsules_data):
    """
    Transform raw capsules data into a format suitable for database loading.
    
    Args:
        capsules_data (list): Raw capsules data from the API
        
    Returns:
        list: Transformed capsule records
    """
    logger.info("Transforming capsules data...")
    
    capsules = []
    
    for capsule in capsules_data:
        if not capsule.get('id'):
            logger.warning("Skipping capsule without ID")
            continue
            
        capsules.append({
            'external_capsule_id': capsule['id'],
            'serial': capsule.get('serial'),
            'type': capsule.get('type'),
            'status': capsule.get('status'),
            'last_update': capsule.get('last_update'),
            'land_landings': capsule.get('land_landings'),
            'water_landings': capsule.get('water_landings'),
            'reuse_count': capsule.get('reuse_count')
        })
    
    logger.info(f"Transformed {len(capsules)} capsules")
    return capsules 