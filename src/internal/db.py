import os
import boto3
from boto3.resources.base import ServiceResource
from dotenv import load_dotenv
import pathlib


base_dir = pathlib.Path(__file__).parent.parent.parent
load_dotenv(base_dir.joinpath('.env')) 


def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
         endpoint_url='http://localhost:8000',
         region_name='example',
         aws_access_key_id='example',
         aws_secret_access_key='example')

    return ddb

def initialize_db_aws() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
         region_name=os.getenv("DB_REGION_NAME_aws"),
         aws_access_key_id=os.getenv("DB_ACCESS_KEY_ID_aws"),
         aws_secret_access_key=os.getenv("DB_SECRET_ACCESS_KEY_aws"),
         aws_session_token=os.getenv("AWS_SESSION_TOKEN"))
    return ddb   

     