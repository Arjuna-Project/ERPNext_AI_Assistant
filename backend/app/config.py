import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
url= os.getenv("url")
