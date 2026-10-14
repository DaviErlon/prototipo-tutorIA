from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE"))
EMAIL_SUPORT = os.getenv("EMAIL_SUPORT")
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))