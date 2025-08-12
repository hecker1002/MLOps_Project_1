
''' 

This is the Dtaa Validation compoent of the robust Ml pieline 

example code --> 

# take the artifatcs ( trian and test csv files form Data iNgestion (prv componet of piepline )) and read file path of schema file 

# class DataValidation : 

    def validate_no_of_cols_schema() : 
    
        status = len( df.columns ) == len( schema["columns"] ) 

    # check if ALL numerical OR caterical columns EXIST or NOT . 

    def is_cols_exists( ) : 
        
        for col in num_cols  : 
            if col not in schema["num_cols"] : 
            raise error 

        for col in cat_cols  : 
            if col not in schema["cat_cols"] : 
            raise error 

    
        

'''


import json
import sys
import os

import pandas as pd

from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):

        try:
            # the trian and test dataset 
            self.data_ingestion_artifact = data_ingestion_artifact

            # the hyeprpam for data validation function 
            self.data_validation_config = data_validation_config

            ''' in entity file , SCHEMA_FILE_PATH = "schema.yaml" path  '''
            self._schema_config =read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)




    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        ''' Just chekcing No. of cols matchign or NOT in trian and test df both 
        '''
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise MyException(e, sys)




    def is_column_exist(self, df: DataFrame) -> bool:
        ''' 
        given column exist or NOT in given df 
        '''
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            # absence of col among Nuemrical cols 
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")

            # absence of cols in Categorical Cols 
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")

            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        except Exception as e:
            raise MyException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)
        

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        RUN ALL the above schema Cross-cehckign and cols-cross chekignand read function to get FINLA VALLDATION STatus and msg . 
        """

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")

            # reading artifacts of Data ingestion (where trianand test dara have saved )
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            '''Checking col len of dataframe for train DATASEZT ) '''
            status = self.validate_number_of_columns(dataframe=train_df)
            
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe. "
            else:
                logging.info(f"All required columns present in training dataframe: {status}")

            ''' NO. of COLUMN inSCHEMA is CORRECT or not in TEST DATASET  '''
            status = self.validate_number_of_columns(dataframe=test_df)

            if not status:
                validation_error_msg += f"Columns are missing in test dataframe. "
            else:
                logging.info(f"All required columns present in testing dataframe: {status}")

            ''' IF COL EXIST or NOT in TRAIN data '''
            status = self.is_column_exist(df=train_df)


            if not status:
                validation_error_msg += f"Columns are missing in training dataframe. "
            else:
                logging.info(f"All categorical/int columns present in training dataframe: {status}")
            

            ''' IF COL EXIST or NOT in TRAIN data '''

            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."
            else:
                logging.info(f"All categorical/int columns present in testing dataframe: {status}")

            validation_status = len(validation_error_msg) == 0

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            # Ensure the directory for validation_report_file_path exists
            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            ''' SAVE the valdation Report at thsisite '''
            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_msg.strip()
            }

            with open(self.data_validation_config.validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)

            logging.info("Data validation artifact created and saved to JSON file.")
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e, sys) from e