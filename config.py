from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = getenv('TOKEN')
MANAGER = int(os.getenv('MANAGER', 0))
