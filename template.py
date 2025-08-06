
import os 
from pathlib import Path 

'''
This file , template.py is just a simple file to make a Project Structure ( folders + files ) for a complicated projrct 
we are about to start , 

so we jsut ned to run thjsi file , in python and it will make all the required folders + fiels inside them . 


-- THIS CODE I PICKED UP ONLINE --- 

'''

# PArent folder 
project_name = "src"


list_of_files = [

    # All the files ( ML modle + trianign + runnign + vladiation + artifacts ) inside src 
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",  
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",

    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/mongo_db_connection.py",

    f"{project_name}/configuration/aws_connection.py",

    f"{project_name}/cloud_storage/__init__.py",
    f"{project_name}/cloud_storage/aws_storage.py",
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/data_access/proj1_data.py",

    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",

    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/estimator.py",

    f"{project_name}/entity/s3_estimator.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipline/__init__.py",

    # combies all compoent of the rosut ML pieplien ( dataingestion + preprocessing + trianign+validation )
    f"{project_name}/pipline/training_pipeline.py",
    f"{project_name}/pipline/prediction_pipeline.py",
    
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",

    # the deployment files + docker files + config files should be outside src folder 
    "app.py",
    "requirements.txt",

    "Dockerfile",
    ".dockerignore",

    "demo.py",
    "setup.py",

    "pyproject.toml",

    "config/model.yaml",
    "config/schema.yaml",
]


for filepath in list_of_files:

    # curr file 
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        # if given file des NOT exist at the ssaid lcoation , crrate it else do NOT touch it . 

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"The given file is already present at: {filepath}")

