import os

from dotenv import load_dotenv

is_docker = os.environ.get('DOCKER_CONTAINER', False)

if is_docker:
    TOKEN = os.environ.get('PROD_TOKEN')
    DEVELOPER_KEY = os.environ.get('YOUTUBE_KEY')
else:
    load_dotenv('boardgamebot.env')
    TOKEN = os.environ.get('DEV_TOKEN')
    DEVELOPER_KEY = os.environ.get('YOUTUBE_KEY')
