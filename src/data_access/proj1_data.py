
''' 
This file used MongoDBCLient() obejct we made to establsih a lcoal PC thing and make coection with DB on mongo DB atlas 

EXAMPLE CODE ---> 
client = MongoDBCLoent( DB_NAME )

# extract the data form afore-said  collection 

data = cleint[ DB_NAME [COLLECTION_NAME ]]

# and convert to PD dataframe ( thec oeltion of KEy-vlaeu apir in NO SQL dB )
df = pd.DataFrame( list( data) )

return df 

else : riase Error( e , sys )

'''
import sys
import pandas as pd
import numpy as np
from typing import Optional

''' This is the LOCAL PACKAGE ( CLASS ) that WE built inside config/mongo coenction file to JSUT make amongoDB client to ESTABLISH conection 
with afore-said DAATABASE '''

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException

# amke it liek a Obejct 
class Proj1Data:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client connection.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        '''
        Under a (Org ->Project -> DB ,Under a colletion ) ,we extratc the key-vlaeu coeltionand covnert to pd.Datfrmae 
        and after some simep,preprceosng return final datasset on which Ml mdoel wil betrianed on 
        '''
        try:
            # Access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Convert collection data to DataFrame and preprocess
            print("Fetching data from mongoDB")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fecthed with len: {len(df)}")

            ''' For ML mdoe trianign  ,w e do NEED ID column '''
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"],   axis=1)
            
            # repalce NA values (null) wit NaN ( not a numebr data type )
            df.replace({"na":np.nan},inplace=True)

            '''final df to train and valdiate our Ml mdoel in Production  ''' 

            return df

        # raise sisue (using logging +exception py file )
        except Exception as e:
            raise MyException(e, sys)