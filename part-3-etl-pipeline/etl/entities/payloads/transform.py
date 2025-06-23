from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def transform_payloads(payloads_data):
    """
    Transform raw payloads data into a format suitable for database loading.
    
    Args:
        payloads_data (list): Raw payloads data from the API
        
    Returns:
        list: Transformed payload records
    """
    logger.info("Transforming payloads data...")
    
    payloads = []
    
    for payload in payloads_data:
        if not payload.get('id'):
            logger.warning("Skipping payload without ID")
            continue
            
        payloads.append({
            'external_payload_id': payload['id'],
            'name': payload.get('name'),
            'type': payload.get('type'),            
            'mass_kg': payload.get('mass_kg'),
            'mass_lbs': payload.get('mass_lbs'),
            'orbit': payload.get('orbit'),
            'reference_system': payload.get('reference_system'),
            'regime': payload.get('regime')            
        })
    
    logger.info(f"Transformed {len(payloads)} payloads")
    return payloads 