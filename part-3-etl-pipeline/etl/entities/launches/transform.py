from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_internal_id_lookup(cursor, table_name, external_id_column):
    """
    Create a lookup dictionary mapping external IDs to internal IDs for a given table.
    
    Args:
        cursor: Database cursor
        table_name (str): Name of the dimension table
        external_id_column (str): Name of the external ID column
        
    Returns:
        dict: Mapping of external_id -> internal_id
    """
    try:
        query = f"SELECT id, {external_id_column} FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
        
        lookup_dict = {row[1]: row[0] for row in results}
        logger.info(f"Created lookup dict for {table_name} with {len(lookup_dict)} entries")
        
        return lookup_dict
    except Exception as e:
        logger.error(f"Error creating lookup for {table_name}: {e}")
        return {}

def transform_launches(launches_data, db_cursor=None):
    """
    Transform raw launches data into a format suitable for database loading.
    
    Args:
        launches_data (list): Raw launches data from the API
        db_cursor: Database cursor for looking up internal IDs (optional)
        
    Returns:
        tuple: (launches, launch_bridge_data)
        where launch_bridge_data is a list of dicts with external_launch_id and bridge records
    """
    logger.info("Transforming launches data...")
    
    launches = []
    launch_bridge_data = []
    
    # Create lookup dictionaries for internal IDs if cursor is provided
    site_lookup = {}
    rocket_lookup = {}
    core_lookup = {}
    payload_lookup = {}
    crew_lookup = {}
    ship_lookup = {}
    capsule_lookup = {}
    landpad_lookup = {}
    
    if db_cursor:
        try:
            site_lookup = get_internal_id_lookup(db_cursor, 'dim_launch_site', 'external_site_id')
            rocket_lookup = get_internal_id_lookup(db_cursor, 'dim_rocket', 'external_rocket_id')
            core_lookup = get_internal_id_lookup(db_cursor, 'dim_core', 'external_core_id')
            payload_lookup = get_internal_id_lookup(db_cursor, 'dim_payload', 'external_payload_id')
            crew_lookup = get_internal_id_lookup(db_cursor, 'dim_crew', 'external_crew_id')
            ship_lookup = get_internal_id_lookup(db_cursor, 'dim_ship', 'external_ship_id')
            capsule_lookup = get_internal_id_lookup(db_cursor, 'dim_capsule', 'external_capsule_id')
            landpad_lookup = get_internal_id_lookup(db_cursor, 'dim_landpad', 'external_landpad_id')
            logger.info("Successfully loaded internal ID lookups")
                        
        except Exception as e:
            logger.warning(f"Could not load internal ID lookups: {e}")
    
    for launch in launches_data:
        if not launch.get('id'):
            logger.warning("Skipping launch without ID")
            continue
            
        # Transform main launch record
        launch_record = {
            'external_launch_id': launch.get('id'),
            'site_id': site_lookup.get(launch.get('launchpad')) if site_lookup else None,
            'rocket_id': rocket_lookup.get(launch.get('rocket')) if rocket_lookup else None,
            'flight_number': launch.get('flight_number'),
            'name': launch.get('name'),
            'details': launch.get('details'),
            'date_utc': launch.get('date_utc'),
            'date_unix': launch.get('date_unix'),
            'date_local': launch.get('date_local'),
            'date_precision': launch.get('date_precision'),            
            'net': launch.get('net'),
            'success': launch.get('success'),
            'launch_window': launch.get('window'),            
            'upcoming': launch.get('upcoming'),                                    
        }

        launches.append(launch_record)
        
        # Store bridge data for this launch
        bridge_data = {
            'external_launch_id': launch.get('id'),
            'cores': [],
            'failures': [],
            'payloads': [],
            'crew': [],
            'ships': [],
            'capsules': []
        }
        
        # Transform core relationships
        for core in launch.get('cores', []):
            if core.get('core'):
                internal_core_id = core_lookup.get(core['core']) if core_lookup else None
                internal_landpad_id = landpad_lookup.get(core.get('landpad')) if landpad_lookup and core.get('landpad') else None
                
                if internal_core_id:  # Only add if we have the internal core ID
                    core_record = {
                        'core_id': internal_core_id,
                        'flight': core.get('flight'),
                        'gridfins': core.get('gridfins'),
                        'legs': core.get('legs'),
                        'reused': core.get('reused'),
                        'landing_attempt': core.get('landing_attempt'),
                        'landing_success': core.get('landing_success'),
                        'landing_type': core.get('landing_type'),
                        'landpad_id': internal_landpad_id
                    }
                    bridge_data['cores'].append(core_record)
        
        # Transform failure relationships - create failure dimension records
        for failure in launch.get('failures', []):
            failure_record = {
                'time': failure.get('time'),
                'altitude': failure.get('altitude'),
                'reason': failure.get('reason')
            }
            bridge_data['failures'].append(failure_record)
        
        # Transform payload relationships
        for payload in launch.get('payloads', []):
            if payload:
                internal_payload_id = payload_lookup.get(payload) if payload_lookup else None
                if internal_payload_id:  # Only add if we have the internal payload ID
                    payload_record = {
                        'payload_id': internal_payload_id
                    }
                    bridge_data['payloads'].append(payload_record)
        
        # Transform crew relationships
        for crew_member in launch.get('crew', []):
            if crew_member:
                internal_crew_id = crew_lookup.get(crew_member) if crew_lookup else None
                if internal_crew_id:  # Only add if we have the internal crew ID
                    crew_record = {
                        'crew_id': internal_crew_id
                    }
                    bridge_data['crew'].append(crew_record)
        
        # Transform ship relationships
        for ship in launch.get('ships', []):
            if ship:
                internal_ship_id = ship_lookup.get(ship) if ship_lookup else None
                if internal_ship_id:  # Only add if we have the internal ship ID
                    ship_record = {
                        'ship_id': internal_ship_id
                    }
                    bridge_data['ships'].append(ship_record)
        
        # Transform capsule relationships
        for capsule in launch.get('capsules', []):
            if capsule:
                internal_capsule_id = capsule_lookup.get(capsule) if capsule_lookup else None
                if internal_capsule_id:  # Only add if we have the internal capsule ID
                    capsule_record = {
                        'capsule_id': internal_capsule_id
                    }
                    bridge_data['capsules'].append(capsule_record)
        
        launch_bridge_data.append(bridge_data)
    
    # Count total bridge records for logging
    total_cores = sum(len(data['cores']) for data in launch_bridge_data)
    total_failures = sum(len(data['failures']) for data in launch_bridge_data)
    total_payloads = sum(len(data['payloads']) for data in launch_bridge_data)
    total_crew = sum(len(data['crew']) for data in launch_bridge_data)
    total_ships = sum(len(data['ships']) for data in launch_bridge_data)
    total_capsules = sum(len(data['capsules']) for data in launch_bridge_data)
    
    logger.info(f"Transformed {len(launches)} launches")
    logger.info(f"Transformed {total_cores} launch-cores relationships")
    logger.info(f"Transformed {total_failures} launch-failures relationships")
    logger.info(f"Transformed {total_payloads} launch-payloads relationships")
    logger.info(f"Transformed {total_crew} launch-crew relationships")
    logger.info(f"Transformed {total_ships} launch-ships relationships")
    logger.info(f"Transformed {total_capsules} launch-capsules relationships")
    
    return (launches, launch_bridge_data) 