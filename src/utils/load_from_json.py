import os
import glob
import json

import toml
from pathlib import Path


# Identify the path to the templates folder
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
config = toml.load(Path(PROJECT_ROOT) / 'config.toml')
output_folder = str(Path(PROJECT_ROOT) / 'src/data_exports')



def load_from_json(name_):

    files = glob.glob(output_folder + '/' + name_ + '*.json')
    latest_file = max(files, key=os.path.getctime)

    with open(latest_file, 'r') as f:
        latest_file_contents = json.load(f)

    return(latest_file_contents)
