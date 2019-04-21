import os

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

# Sentry.io URL
sentry_url = os.environ.get('SENTRY_URL')
