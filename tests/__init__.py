import sys
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR_NAME = 'backend'
MAIN_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
sys.path.append(MAIN_PATH)
