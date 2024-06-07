import os
import utils.config


def is_dev_env():
    MODE = os.getenv("MODE")
    return MODE == "development"