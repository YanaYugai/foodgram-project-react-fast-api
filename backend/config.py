import os
from typing import cast

from dotenv import load_dotenv

load_dotenv()

DB_HOST = cast(str, os.getenv('DB_HOST'))
DB_PORT = cast(str, os.getenv('DB_PORT'))
DB_NAME = cast(str, os.getenv('DB_NAME'))
DB_USER = cast(str, os.getenv('DB_USER'))
DB_PASS = cast(str, os.getenv('DB_PASS'))
SECRET_KEY = cast(str, os.getenv('SECRET_KEY'))
