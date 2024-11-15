import os
from dotenv import load_dotenv

if not os.getenv('DOCKERIZED'):
    load_dotenv()

MODEL_TYPE = os.getenv("MODEL_TYPE")
# where the bot stores the file to process
BOT_FOLDER = os.getenv("BOT_FOLDER")
MODE = os.getenv("MODE")

MY_ID = int(os.getenv("MY_ID"))
TOKEN_API = os.getenv("TOKEN_API")
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE"))
MESSAGE_MAX_LEN_WITHOUT_FILE = int(os.getenv("MESSAGE_MAX_LEN_WITHOUT_FILE"))

assert MODEL_TYPE in ("tiny", "base", "small", "medium", "large", "turbo"), "Invalid model type"
