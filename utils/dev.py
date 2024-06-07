import os
import dotenv
dotenv.load_dotenv()


def is_dev_env():
    MODE = os.getenv("MODE")
    return MODE == "development"