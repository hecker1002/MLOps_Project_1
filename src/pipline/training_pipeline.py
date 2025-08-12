
''' 

the ACTUAL code that calls all the relevant methods of DS life cycel of proect to pull dta
 precproces it trian Ml mdoel on it hyerpa tunign etc 

 (0only the code to run Dtaa ingestion ONLY for now )
'''

import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher 

''' DataINgestion zconfig --> has file apth for the dataset itnermedoate '''
from src.entity.config_entity import (DataIngestionConfig  ,
                                      DataValidationConfig , 
                                      DataTransformationConfig  , 
                                      ModelTrainerConfig , 
                                      ModelEvaluationConfig , 
                                      ModelPusherConfig
                                      ) 
                                         
''' dataingestion aritfact ---> stores the file path of the artifact ( trian andtest data path ) wehre they finalfiles wil besaved '''                    
from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataValidationArtifact , 
                                        DataTransformationArtifact  , 
                                        ModelTrainerArtifact , 
                                        ModelEvaluationArtifact , 
                                        ModelPusherArtifact
                                        )
                                           


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

        self.data_validation_config = DataValidationConfig()
        
        self.data_transformation_config = DataTransformationConfig()

        self.model_trainer_config = ModelTrainerConfig()

        self.model_evaluation_config = ModelEvaluationConfig()

        self.model_pusher_config  =  ModelPusherConfig()

    
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
        
    ''' data valudation '''

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        ''' Validates thta the trian and test df have corect columns , schema and presence of columns . '''

        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config
                                             )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")

            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
    


    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        
        except Exception as e:
            raise MyException(e, sys)
    

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys)
        
    ''' Model Evaluation '''
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        """
        This method of TrainPipeline class is responsible for starting modle evaluation
        """
        try:
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys)

    # statrt pushing Mdoel to S3 bucket with given S3 bucket file path ( on AWS )
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """
        This method of TrainPipeline class is responsible for starting model pushing
        """
        try:
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                       model_pusher_config=self.model_pusher_config
                                       )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    def run_pipeline(self, ) -> None:
        ''' 
        Run the Dta ingestion compoent ONLY of the piepline 
        '''
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation( data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            
            # start modle training 
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            # evlauting the mdoel (and comapring results with the model saved on the S3 bucket )
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            
            ''' Put a condition to push te model ovnly if it Betetr ( f1 score om X_tets ) than model alreayd saved on S3 bucke t'''
            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model not accepted as it does NOT have better F1 score than prev saved model on S3  .")
                return None
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)

        except Exception as e:
            raise MyException(e, sys)