import os
import psycopg2

from dotenv import load_dotenv

is_docker = os.environ.get('DOCKER_CONTAINER', False)

# Uses python-dotenv package to load env file if not running in docker
if not is_docker:
    load_dotenv('boardgamebot.env')

# Sets token for discord bot
if is_docker:
    TOKEN = os.environ.get('PROD_TOKEN')
else:
    TOKEN = os.environ.get('DEV_TOKEN')

# Youtube key, same for both environments
DEVELOPER_KEY = os.environ.get('YOUTUBE_KEY')

# Database configuration
if is_docker:
    HOST = os.environ.get('PROD_DB_HOST')
    DATABASE = os.environ.get('PROD_DB_NAME')
    USER = os.environ.get('PROD_DB_USER')
    PASSWORD = os.environ.get('PROD_DB_PASSWORD')
else:
    HOST = os.environ.get('DEV_DB_HOST')
    DATABASE = os.environ.get('DEV_DB_NAME')
    USER = os.environ.get('DEV_DB_USER')
    PASSWORD = os.environ.get('DEV_DB_PASSWORD')

