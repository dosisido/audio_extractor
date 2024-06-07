import os
from dotenv import load_dotenv

if not os.getenv('DOCKERIZED'):
    load_dotenv()