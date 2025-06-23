import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def transform_company(company_data):
    """
    Transform raw company data into a format suitable for database loading.
    
    Args:
        company_data (dict): Raw company data from the API
        
    Returns:
        dict: Transformed company record
    """
    logger.info("Transforming company data...")
    
    if not company_data.get('id'):
        logger.error("Company data missing ID")
        raise ValueError("Company data must contain an ID")
    
    company = {
        'external_company_id': company_data['id'],
        'name': company_data.get('name'),
        'founder': company_data.get('founder'),
        'founded': company_data.get('founded'),
        'employees': company_data.get('employees'),
        'vehicles': company_data.get('vehicles'),
        'launch_sites': company_data.get('launch_sites'),
        'test_sites': company_data.get('test_sites'),
        'ceo': company_data.get('ceo'),
        'cto': company_data.get('cto'),
        'coo': company_data.get('coo'),
        'cto_propulsion': company_data.get('cto_propulsion'),
        'valuation': company_data.get('valuation'),
        'summary': company_data.get('summary')
    }
    
    logger.info("Company data transformed successfully")
    return company 
