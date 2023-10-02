# Import required modules
import logging
from pathlib import Path
from datetime import datetime
import os

# Function to setup logging
def setup_logging():
    # Get project root from environment variable
    PROJECT_ROOT = os.getenv("PROJECT_ROOT")
    
    # Create logs directory if doesn't exist
    log_dir = Path(PROJECT_ROOT) / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        filename=Path(PROJECT_ROOT) / 'logs' / f"log_{datetime.now().strftime('%Y%m%d')}.txt",
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Get or create logger
    logger = logging.getLogger()
    
    # Add stream handler if not exists
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())