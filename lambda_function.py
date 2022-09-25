import os
import sys
import logging
import boto3
import re
from datetime import datetime
from hz_catch_utils import get_color_map, finalize_ifc

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']
BASE_URL = os.environ['CATCH_URL']
SERVICE_ACCOUNT_USERNAME = os.environ['SERVICE_ACCOUNT_USERNAME']
SERVICE_ACCOUNT_PASSWORD = os.environ['SERVICE_ACCOUNT_PASSWORD']
#IfcColorizerTest
#IfcColorizerStaging
#IfcColorizerProd

s3 = boto3.client('s3')

def lambda_handler(event, context):
    file_key = event['file_key']
    ifc_file_id = int(event['ifc_file_id'])    
    errored = False
    
    logger.info(f'IFC Colorizer for file name [{file_key}] with id [{ifc_file_id}]')
    
    #Get the original IFC
    try:
        temp_filename = 'ifc_' + datetime.utcnow().strftime('%Y%m%d%H%M%S') + '.ifc'
        temp_filepath = os.path.join('/tmp', temp_filename)
        colorized_temp_filename =  'ifc_colorized_' + datetime.utcnow().strftime('%Y%m%d%H%M%S') + '.ifc'
        colorized_temp_filepath = os.path.join('/tmp', colorized_temp_filename)
        s3.download_file(S3_BUCKET, file_key, temp_filepath)
    except:
        errored = True
        logger.error('An error occurred while downloading original IFC', exc_info=sys.exc_info())        

    #persist the original in S3    
    if not errored:
        try:
            with open(temp_filepath, 'rb') as ifc_binary_content:
                s3.upload_fileobj(ifc_binary_content, S3_BUCKET, file_key.split('.')[0] + "_original.ifc")
        except:
            errored = True
            logger.error('An error occurred while saving original IFC', exc_info=sys.exc_info())        
    
    #Loads the color map from Catch
    if not errored:
        colors = get_color_map(BASE_URL, SERVICE_ACCOUNT_USERNAME, SERVICE_ACCOUNT_PASSWORD)
        color_map = colors['color_map']   
        fallback_color=colors['fallback_color']
    
    #Apply the color map, using the fallback color for any colors not in the map
    if not errored:
        try:
            with open(temp_filepath, 'r') as original_file, open(colorized_temp_filepath, 'a') as colorized_file:
                for line in original_file:
                    if re.match('.*IFCCOLOURRGB\(\$,((\d\.\d*)(|,)){3}\);', line):
                        replaced_color = False
                        for mapped_color in color_map:
                            if mapped_color['inval'] in line:
                                logger.info(f'Replacing line -- {line}')
                                replaced_color = True
                                line = line.replace(mapped_color['inval'], mapped_color['outval'])
                        if not replaced_color:
                            logger.info(f'Using fallback color for line -- {line}')
                            line = line.replace(mapped_color['inval'], fallback_color)
                    colorized_file.write(line)
        except:
            logger.error('An error occurred while colorizing IFC', exc_info=sys.exc_info())
            errored = True
    
    #Upload the colorized IFC to S3 by replacing the original
    if not errored:
        try:
            s3.upload_file(colorized_temp_filepath, S3_BUCKET, file_key)
        except:
            logger.error('An error occurred while uploading colorized IFC', exc_info=sys.exc_info())
            errored = True
    
    finalize_ifc(BASE_URL, SERVICE_ACCOUNT_USERNAME, SERVICE_ACCOUNT_PASSWORD, ifc_file_id, 'error' if errored else 'complete')