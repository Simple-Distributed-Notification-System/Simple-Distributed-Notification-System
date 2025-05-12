from dotenv import load_dotenv
import os

# Takes the things .env files and encrypts them


load_dotenv()  

MONGODB_URI_LOCAL = os.getenv("MONGODB_URI_LOCAL")
MONGODB_URI_REMOTE = os.getenv("MONGODB_URI_REMOTE")
ID_SERVER = os.getenv("ID_SERVER")
SERVER_URL = os.getenv("SERVER_URL")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
