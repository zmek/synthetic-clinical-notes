
# Script to load A&E Synthetic Data into a Pandas DataFrame
# 
# Inputs: None
# Outputs: Pandas DataFrame saved in Parquet format
#
# Requires:
# - Python Standard Libraries: sys, os, warnings, datetime, logging
# - Third-Party Libraries: toml, pathlib, pandas, requests, py7zr
# - Custom Libraries: init

import sys
import os
import toml
from pathlib import Path
import pandas as pd
import warnings
import requests
import py7zr
import logging
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
import init

def load_file():
    PROJECT_ROOT = os.getenv("PROJECT_ROOT")
    config = toml.load(Path(PROJECT_ROOT) / 'config.toml')

    # Define paths
    DATA_STORE_PATH = Path(config['Paths']['DATA_STORE_PATH'])
    zip_file_path = DATA_STORE_PATH / 'A&E+Synthetic+Data.7z'
    csv_file_path = DATA_STORE_PATH / 'A&E Synthetic Data.csv'
    parquet_file_path = DATA_STORE_PATH / 'A&E+Synthetic+Data.parquet'
    icd10_file_path = PROJECT_ROOT + '/src/data_ingestion/icd10_lookup.csv'

    # Setup logging
    log_dir = Path(PROJECT_ROOT) / 'logs'
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO,
                        filename=Path(PROJECT_ROOT) / 'logs' / f"log_{datetime.now().strftime('%Y%m%d')}.txt",
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    # Check if logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
        
    # Check and load data
    if not os.path.exists(parquet_file_path):
        if not os.path.exists(zip_file_path):
            # Download zip file
            warnings.warn('Synthetic data not found. Downloading.')
            url = 'https://nhsengland-direct-uploads.s3-eu-west-1.amazonaws.com/A%26E+Synthetic+Data.7z?versionId=null'
            try:
                r = requests.get(url)
                r.raise_for_status()
                with open(zip_file_path, 'wb') as f:
                    f.write(r.content)
                logger.info("Saved zip file.")
            except requests.RequestException as e:
                logger.error(f'Error: {e}')

        # Unzip file
        if not os.path.exists(csv_file_path):
            try:
                with py7zr.SevenZipFile(zip_file_path, mode='r') as z:
                    z.extractall(path=os.path.dirname(csv_file_path))
                logger.info("Saved unzipped csv.")
            except Exception as e:
                logger.error(e)

        # Load csv, filter, save as parquet
        logger.info("Reading unzipped csv.")
        ed = pd.read_csv(csv_file_path)
        ed = ed.query("Length_Of_Stay_Days > 1 and Admitted_Flag == 1")
        try:
            ed.to_parquet(parquet_file_path)
            logger.info(f"Saved parquet file, shape: {ed.shape}")
        except Exception as e:
            logger.error(e)

        # Load ICD10 lookup and merge with ed to include a description of the ICD10 code
        icd = pd.read_csv(icd10_file_path)
        ed = ed.merge(icd, left_on='ICD10_Chapter_Code', right_on='Chapter')
        logger.info(f"Merged ED file with ICD10 lookup")

        ed.to_parquet(parquet_file_path)
        logger.info(f"Saved parquet file, shape: {ed.shape}")

    else:
        # Load existing parquet file
        ed = pd.read_parquet(parquet_file_path)
        logger.info(f"Loaded parquet file, shape: {ed.shape}")

    return ed
