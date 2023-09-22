from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Set PROJECT_ROOT
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.environ["PROJECT_ROOT"] = PROJECT_ROOT

