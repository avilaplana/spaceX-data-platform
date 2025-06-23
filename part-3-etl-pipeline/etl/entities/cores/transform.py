from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def transform_cores(data):
    """
    Transform core data from the SpaceX API into our database format.
    
    Args:
        data (list): Raw core data from the API
        
    Returns:
        list: List of transformed core records
    """
    logger.info("Starting transformation of core data...")
    
    cores = []
    for core in data:
        core_id = core.get('id')
        if not core_id:
            continue
            
        cores.append({
            'external_core_id': core_id,
            'serial': core.get('serial'),
            'block': core.get('block'),
            'status': core.get('status'),
            'reuse_count': core.get('reuse_count'),
            'rtls_attempts': core.get('rtls_attempts'),
            'rtls_landings': core.get('rtls_landings'),
            'asds_attempts': core.get('asds_attempts'),
            'asds_landings': core.get('asds_landings'),
            'last_update': core.get('last_update'),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })
    
    logger.info(f"Transformed {len(cores)} cores")
    return cores 