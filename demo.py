
''' 

THis file will be used to run and debug codes beforesending in prodcutuion online 
'''

from src.pipline.training_pipeline  import TrainPipeline

pipeline = TrainPipeline()
pipeline.run_pipeline( )

