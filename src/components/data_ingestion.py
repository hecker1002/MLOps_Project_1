'''
Data Ingestion file ---> Pull the Data using Mongo CLient and stores it  as pd Datafrmae and then performs trin test split on it 
and stores thes trian test data at specific path in the same project . 

Dtaa ingestion <----> config_entity(for var names ) <----> ( cosnatnt.py for value of var all are talkign toeach other )

Exampel code 

clas DataIngestion : 

    def export_df_mongoDB (self ) : 
        df = Proj1_data ( mongoclient(url ))
        return df 

    def train_test_split( self , df , rstio  ) : 
        train_csv , test_csv = trian_test_split( df , ratio )

        return save_At_dir_path(trian_csv , trst_csv )

    def call_df_trian_test ( self ) : 
        df = export_df( )

        final_df_train ,final_df_test = train_test_split( df , ratio = config_entity-->cosntant.py  )

        return final_df_train ,final_df_test 
    

'''

import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import MyException
from src.logger import logging
from src.data_access.proj1_data import Proj1Data

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
        

    def export_data_into_feature_store(self)->DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info(f"Exporting data from mongodb")

            # Proj1-data ( used mong client ( mongodb_conenctio_url )) to amke a lcoal PC and conect to mongo db db cluster an d
            # PULL data from there and stores it as pd Dataframe 

            my_data = Proj1Data()
            dataframe = my_data.export_collection_as_dataframe(collection_name=
                                                                   self.data_ingestion_config.collection_name)
            
            logging.info(f"Shape of dataframe: {dataframe.shape}")

            feature_store_file_path  = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            
            return dataframe

        except Exception as e:
            raise MyException(e,sys)

    def split_data_as_train_test(self,dataframe: DataFrame) ->None:
        '''
        we split the returned Dataframe based on split ratio stored in config file 
        
        '''

        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

            logging.info("Performed train test split on the dataframe accoridng to given split ratio ")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            ''' Saving the csv trian test dataset to correct apths in project '''
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise MyException(e, sys) from e

    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:

            ''' Call the above fucntions ( of pullign data + trian test split + save togther here )'''
            dataframe = self.export_data_into_feature_store()

            logging.info("Got the data from mongodb")

            self.split_data_as_train_test(dataframe)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            ''' the prdocut of data ingestion (triantest fiel also Saved )'''
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys) from e