import os
from dotenv import load_dotenv

if not os.getenv('DOCKERIZED'):
    load_dotenv()

MODEL_TYPE = os.getenv("MODEL_TYPE")
TRANSCRIBER_FOLDER = os.getenv("TRANSCRIBER_FOLDER")
BOT_FOLDER = os.getenv("BOT_FOLDER")
MODE = os.getenv("MODE")

MY_ID = os.getenv("MY_ID")
TOKEN_API = os.getenv("TOKEN_API")
MAX_QUEUE_SIZE = os.getenv("MAX_QUEUE_SIZE")

assert TRANSCRIBER_FOLDER.endswith("cache"), "TMP_FOLDER must end with 'cache'"
assert MODEL_TYPE in ("tiny", "base", "small", "medium", "large"), "Invalid model type"
