import logging
import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

def load_launches(conn, launches_data, launch_bridge_data):
    """
    Load transformed launches data into the database.
    
    Args:
        conn: Database connection
        launches_data (list): Transformed launches records
        launch_bridge_data (list): List of dicts with external_launch_id and bridge records
    """
    logger.info("Loading launches data into database...")
    
    try:
        with conn.cursor() as cur:
            # Clear existing data
            logger.info("Clearing existing launches data...")
            cur.execute("""
                TRUNCATE TABLE 
                    fact_launches,
                    bridge_launch_core,
                    bridge_launch_failure,
                    bridge_launch_payload,
                    bridge_launch_crew,
                    bridge_launch_ship,
                    bridge_launch_capsule
                CASCADE
            """)
            
            # Load launches data first and create mapping
            launch_id_mapping = {}  # external_launch_id -> internal_launch_id
            if launches_data:
                logger.info(f"Loading {len(launches_data)} launches records...")
                
                # Insert launches and get their internal IDs
                for launch_record in launches_data:
                    external_launch_id = launch_record['external_launch_id']
                    
                    # Insert the launch record
                    columns = list(launch_record.keys())
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO fact_launches ({', '.join(columns)})
                        VALUES ({placeholders})
                        RETURNING id
                    """
                    values = [launch_record[col] for col in columns]
                    cur.execute(query, values)
                    
                    # Get the internal launch ID
                    internal_launch_id = cur.fetchone()[0]
                    launch_id_mapping[external_launch_id] = internal_launch_id
                
                logger.info(f"Launches data loaded successfully. Created {len(launch_id_mapping)} launch ID mappings")
            else:
                logger.warning("No launches data to load")
            
            # Load failures into dim_failure table first
            failure_id_mapping = {}  # failure_data -> internal_failure_id
            all_failures = []
            for bridge_data in launch_bridge_data:
                all_failures.extend(bridge_data['failures'])
            
            if all_failures:
                logger.info(f"Loading {len(all_failures)} failure records...")
                
                for failure_record in all_failures:
                    # Insert failure into dim_failure
                    columns = ['time', 'altitude', 'reason']
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO dim_failure ({', '.join(columns)})
                        VALUES ({placeholders})
                        RETURNING id
                    """
                    values = [failure_record[col] for col in columns]
                    cur.execute(query, values)
                    
                    # Get the internal failure ID
                    internal_failure_id = cur.fetchone()[0]
                    
                    # Create a key for the failure record (time + altitude + reason)
                    failure_key = (failure_record.get('time'), failure_record.get('altitude'), failure_record.get('reason'))
                    failure_id_mapping[failure_key] = internal_failure_id
                
                logger.info(f"Failure records loaded successfully. Created {len(failure_id_mapping)} failure ID mappings")
            
            # Load bridge table relationships
            total_cores = 0
            total_payloads = 0
            total_crew = 0
            total_ships = 0
            total_capsules = 0
            total_failures = 0
            
            for bridge_data in launch_bridge_data:
                external_launch_id = bridge_data['external_launch_id']
                if external_launch_id not in launch_id_mapping:
                    logger.warning(f"No internal launch ID found for external_launch_id: {external_launch_id}")
                    continue
                
                internal_launch_id = launch_id_mapping[external_launch_id]
                
                # Load core relationships
                for core_record in bridge_data['cores']:
                    record_with_launch_id = {**core_record, 'launch_id': internal_launch_id}
                    columns = list(record_with_launch_id.keys())
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO bridge_launch_core ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    values = [record_with_launch_id[col] for col in columns]
                    cur.execute(query, values)
                    total_cores += 1
                
                # Load failure relationships
                for failure_record in bridge_data['failures']:
                    failure_key = (failure_record.get('time'), failure_record.get('altitude'), failure_record.get('reason'))
                    if failure_key in failure_id_mapping:
                        internal_failure_id = failure_id_mapping[failure_key]
                        cur.execute("""
                            INSERT INTO bridge_launch_failure (launch_id, failure_id)
                            VALUES (%s, %s)
                        """, (internal_launch_id, internal_failure_id))
                        total_failures += 1
                
                # Load payload relationships
                for payload_record in bridge_data['payloads']:
                    record_with_launch_id = {**payload_record, 'launch_id': internal_launch_id}
                    columns = list(record_with_launch_id.keys())
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO bridge_launch_payload ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    values = [record_with_launch_id[col] for col in columns]
                    cur.execute(query, values)
                    total_payloads += 1
                
                # Load crew relationships
                for crew_record in bridge_data['crew']:
                    record_with_launch_id = {**crew_record, 'launch_id': internal_launch_id}
                    columns = list(record_with_launch_id.keys())
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO bridge_launch_crew ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    values = [record_with_launch_id[col] for col in columns]
                    cur.execute(query, values)
                    total_crew += 1
                
                # Load ship relationships
                for ship_record in bridge_data['ships']:
                    record_with_launch_id = {**ship_record, 'launch_id': internal_launch_id}
                    columns = list(record_with_launch_id.keys())
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO bridge_launch_ship ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    values = [record_with_launch_id[col] for col in columns]
                    cur.execute(query, values)
                    total_ships += 1
                
                # Load capsule relationships
                for capsule_record in bridge_data['capsules']:
                    record_with_launch_id = {**capsule_record, 'launch_id': internal_launch_id}
                    columns = list(record_with_launch_id.keys())
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"""
                        INSERT INTO bridge_launch_capsule ({', '.join(columns)})
                        VALUES ({placeholders})
                    """
                    values = [record_with_launch_id[col] for col in columns]
                    cur.execute(query, values)
                    total_capsules += 1
            
            logger.info(f"Bridge relationships loaded successfully:")
            logger.info(f"  - {total_cores} launch-cores relationships")
            logger.info(f"  - {total_failures} launch-failures relationships")
            logger.info(f"  - {total_payloads} launch-payloads relationships")
            logger.info(f"  - {total_crew} launch-crew relationships")
            logger.info(f"  - {total_ships} launch-ships relationships")
            logger.info(f"  - {total_capsules} launch-capsules relationships")
            
            conn.commit()
            logger.info("Launches data loading completed successfully")
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading launches data: {str(e)}")
        raise 