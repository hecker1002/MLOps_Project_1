

import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    ''' 
        MongoCLinet ---> a class made by use when intializrd wil act like a simple local system to set UP conection with 
        the given DATABASE ( no sql hsoted on Mongo DB atlas ) and we can pul data from there . 

        Exampel code --> 

        # def __init__(self , database_name ) : 

    #     if MongoDBClient.client==None : 
    #         mongo_db_url = os.getenv( mongo_db_conenction_key)

    #         if mongo_db_conenction_key==Null : 
    #             raise Exception()
    #         #d efine the database  
    #         self.client.database[ colletion]
    #         client  = pymongo.MongoClient( mongo_db_conn ectio key , tlscafile = ca # reuqire for cerification authoriarion )

     this pymongo.MongoCleint( coonection key ,ca )-> use conection eky to establish coention with mongo DBdatabase and coletion inside it 
     and use CA certifcati that we apse in tlsCAfile to acces it asily and  safely 

    #  the DATABSE NAME for this cleint ( wewil pick the cosntant DB anme from constant.init py file ) reduced reducnadncy :) 
    '''

    client = None  # Shared MongoClient instance across all MongoDBClient instances

    


    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name :
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        try:
            # Check if a MongoDB client connection has already been established; if not, create a new one
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)  # Retrieve MongoDB URL from environment variables
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                
                # Establish a new MongoDB client connection
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
            # Use the shared MongoClient for this instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name]  # Connect to the specified database
            self.database_name = database_name
            logging.info("MongoDB connection successful.")
            
        except Exception as e:
            # Raise a custom exception with traceback details if connection fails
            raise MyException(e, sys)
        

