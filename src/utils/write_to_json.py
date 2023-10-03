import json
from datetime import datetime
import toml
import os   
from pathlib import Path


# Identify the path to the templates folder
PROJECT_ROOT = os.getenv("PROJECT_ROOT")
config = toml.load(Path(PROJECT_ROOT) / 'config.toml')
output_folder = str(Path(PROJECT_ROOT) / 'src/data_exports')


def write_to_json(data, name_):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{output_folder}/{name_}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f)
