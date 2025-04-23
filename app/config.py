# config.py

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

MONGODB_URI_LOCAL = os.getenv("MONGODB_URI_LOCAL")
MONGODB_URI_REMOTE = os.getenv("MONGODB_URI_REMOTE")
ID_SERVER = os.getenv("ID_SERVER")
SERVER_URL = os.getenv("SERVER_URL")
