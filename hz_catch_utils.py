import sys
import logging
import requests
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_color_map(base_url, username, password):    
    logger.info(f'GETing color map')
    session = requests.Session()
    
    #Log in so we get a cookie
    logger.info(f'Authenticating with Catch')
    auth_response = session.post(base_url + 'api/users/login', json={'username': username, 'password': password})
    if(auth_response.status_code != 200):
        logger.info(f'Received non-success status of {auth_response.status_code} authenticating with Catch: {json.dumps(auth_response.json())}')
        raise Exception('Unable to authenticate with Catch. Got status: '+ auth_response.status_code)
    
    #Get the variable
    logger.info(f'GETing config var')
    config_response = session.get(base_url + 'api/configvars/ifc_color_map')
    
    logger.info(f'GET config var completed with status {config_response.status_code}')
    logger.info(f'GET config var response body {json.dumps(config_response.json())}')
    if(config_response.status_code != 200):
        logger.info(f'Received non-success status of {config_response.status_code} getting config var from Catch: {json.dumps(config_response.json())}')
        raise Exception('GET config var Received non-success status of ' + str(config_response.status_code))
    
    try:
        colors = json.loads(config_response.json()['config_var']['var_value'])
    except:
        logger.error('An error occurred reading config var data', exc_info=sys.exc_info())
        raise Exception('An error occurred reading config var data')
    return colors

def finalize_ifc(base_url, username, password, ifc_file_id, status):    
    logger.info(f'POSTing to Catch to finalize job')
    session = requests.Session()
    
    #Log in so we get a cookie
    logger.info(f'Authenticating with Catch')
    auth_response = session.post(base_url + 'api/users/login', json={'username': username, 'password': password})
    if(auth_response.status_code != 200):
        #log the error?
        logger.info(f'Received non-success status of {auth_response.status_code} authenticating with Catch: {json.dumps(auth_response.json())}')
        raise Exception('Unable to authenticate with Catch. Got status: '+ auth_response.status_code)
    
    #Finalize the IFC parse
    logger.info(f'Finalizing job with Catch')
    finish_response = session.post(base_url + 'api/ifc/finish_color', json={"ifc_file_id": ifc_file_id, "status": status})
    
    logger.info(f'Finalize job completed with status {finish_response.status_code}')
    logger.info(f'Finalize job completed with response body {json.dumps(finish_response.json())}')
    
