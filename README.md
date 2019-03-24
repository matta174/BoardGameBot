# BoardGameBot
This is the repository for a board game Discord bot

Confused? Click [here](https://www.quora.com/What-is-a-discord-bot-What-is-a-discord-server)

### Prerequisites
#### What things you need to install: 
discord - [link](https://github.com/Rapptz/discord.py)

boardgamegeek - [link](https://github.com/lcosmin/boardgamegeek)

Google APIs Client Library for Python - [link](https://developers.google.com/api-client-library/python/start/installation)

#### How to install them:

>pip install discord

>pip install boardgamegeek2

>pip install google-api-python-client

>pip install python-env

### Using the bot

* Create a new Discord Application [here](https://discordapp.com/developers/applications/) 

* After creating the app on the app details page scroll down to the Bot page and create a bot.

* Save the token for the bot

* Go to this url https://discordapp.com/oauth2/authorize?client_id=XXXXXXXXXXXX&scope=bot and replace the client id with your app's client ID and authorize your app

* replace the token in main.py with your token and run




### Commands
| Name        | Description           | Command  |
| :-------------: |:-------------:| :-----:|
| BGGCheck      | Returns the BoardGameGeek.com  information of a specified game | `!bg *game name*` |
| Random_Game     | Returns a random game title from a provided list      |   `!rbg *list of games*` |
| HowToPlay | Returns the top search result video from YouTube on how to play |    `!htp *game name*` |
| Lookup_BGG_User| Lookup a board game geek user's game collection  | `!go *username*` |
|Random_Owned_Game |Returns a random game title from a user's owned list | `!robg *username*`|
| Game_Ambiance | Returns the top search result video for selected topic from YouTube | `!amb *topic*` |

