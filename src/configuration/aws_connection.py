
'''

AWS ( amazon Web services ) - it provides cloud services to users . 
there isa root user who is maintian somethifn on this cloud service and 
we create IAM users , ( who  with their credentiala (acces key , password ))
can have some access (as defined by root user ) of the app / servce hosted on AWS 

AWS S3 bucket --> like a Google drive (storage ) for AWS for diff data 

Here , other code is making an S3 bucket and connecting to it using ( by acting as IAm user and its credentials )
(just like pymongo client conenction string )

boto3 --> python lib to manage diff AWS services  from code directly 

example code --> 

resource = boto3.resource ( 's3' , aws_acces_key , aws_secret_acces_key , region_name )
client  = boto3.client( 's3' , aws_acces_key , aws_secret-acces_key , region_name )

retirn resource , cleint 

'''
import boto3
import os

''' IAM user Login credentials '''
from src.constants import AWS_SECRET_ACCESS_KEY_ENV_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, REGION_NAME


class S3Client:

    s3_client=None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        """ 
        This Class gets aws credentials from env_variable and creates an connection with s3 bucket 
        and raise exception when environment variable  ( acces id and apsskey of IAm  user ) is not set
        """

        if S3Client.s3_resource==None or S3Client.s3_client==None:

            ''' These are login creddc so must be PRIVATE VARIABLES ( should NOT be accessed outside the class so _ _ var_name )'''
            __access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY, )
            __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY, )

            if __access_key_id is None:
                raise Exception(f"Environment variable: {AWS_ACCESS_KEY_ID_ENV_KEY} is not not set.")
            if __secret_access_key is None:
                raise Exception(f"Environment variable: {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set.")
        
            S3Client.s3_resource = boto3.resource('s3',
                                            aws_access_key_id=__access_key_id,
                                            aws_secret_access_key=__secret_access_key,
                                            region_name=region_name
                                            )
            S3Client.s3_client = boto3.client('s3',
                                        aws_access_key_id=__access_key_id,
                                        aws_secret_access_key=__secret_access_key,
                                        region_name=region_name
                                        )
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client
