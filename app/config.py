from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

MONGODB_URI_LOCAL = os.getenv("MONGODB_URI_LOCAL")
ID_SERVER = os.getenv("ID_SERVER")
SERVER_URL = os.getenv("SERVER_URL")
