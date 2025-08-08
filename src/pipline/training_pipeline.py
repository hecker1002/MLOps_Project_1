
''' 

the ACTUAL code that calls all the relevant methods of DS life cycel of proect to pull dta
 precproces it trian Ml mdoel on it hyerpa tunign etc 

 (0only the code to run Dtaa ingestion ONLY for now )
'''

import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion


''' DataINgestion zconfig --> has file apth for the dataset itnermedoate '''
from src.entity.config_entity import (DataIngestionConfig) 
                                         
''' dataingestion aritfact ---> stores the file path of the artifact ( trian andtest data path ) wehre theyfinalfiles wil besaved '''                    
from src.entity.artifact_entity import (DataIngestionArtifact)
                                           


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        

    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        ''' 
        call  mongodb client and pull data from mogn db atlas 
        '''
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")

            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        
    
    def run_pipeline(self, ) -> None:
        ''' 
        Run the Dta ingestion compoent ONLY of the piepline 
        '''
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
        except Exception as e:
            raise MyException(e, sys)