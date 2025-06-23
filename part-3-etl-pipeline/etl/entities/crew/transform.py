import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def transform_crew(crew_data):
    """
    Transform raw crew data into a format suitable for database loading.
    
    Args:
        crew_data (list): Raw crew data from the API
        
    Returns:
        list: Transformed crew records
    """
    logger.info("Transforming crew data...")
    
    crew = []
    
    for member in crew_data:
        if not member.get('id'):
            logger.warning("Skipping crew member without ID")
            continue
            
        crew.append({
            'external_crew_id': member['id'],
            'name': member.get('name'),
            'status': member.get('status'),
            'agency': member.get('agency'),
            'image': member.get('image'),
            'wikipedia': member.get('wikipedia')
        })
    
    logger.info(f"Transformed {len(crew)} crew members")
    return crew 