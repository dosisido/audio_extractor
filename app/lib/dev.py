from lib.config import MODE


def is_dev_env():
    return MODE == "development"