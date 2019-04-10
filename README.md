# BoardGameBot
This is the repository for a board game Discord bot

[![star this repo](http://githubbadges.com/star.svg?user=matta174&repo=BoardGameBot&style=default)](https://github.com/matta174/BoardGameBot)   [![fork this repo](http://githubbadges.com/fork.svg?user=matta174&repo=BoardGameBot&style=default)](https://github.com/matta174/BoardGameBot/fork)  [![Python 3.6.7](https://img.shields.io/badge/python-3.6.7-blue.svg)](https://www.python.org/downloads/release/python-360/)  ![GitHub repo size](https://img.shields.io/github/repo-size/matta174/boardgamebot.svg)    ![Discord](https://img.shields.io/discord/288694246721191947.svg)   ![GitHub issues](https://img.shields.io/github/issues-raw/matta174/boardgamebot.svg)    ![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/boardgamebot/boardgamebot.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/matta174/boardgamebot/badge)](https://www.codefactor.io/repository/github/matta174/boardgamebot)



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

>pip install psycopg2

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
|Random_Owned_Game |Returns a random game title from a user's owned list | `!robg *username*`|
|What_Game_Can_We_Play |Looks up a user's game collection and how many people are playing to see what games you could play |`!wcwp *username*, *number of players* `|
| HowToPlay | Returns the top search result video from YouTube on how to play |    `!htp *game name*` |
| Game_Ambiance | Returns the top search result video for selected topic from YouTube | `!amb *topic*` |
| Next_Video | Returns the next video in the last youtube search | `!nxt` |
| Expansion_Check | Returns expansions for the selected game if they exist | `!exp *game name*` |
| Lookup_BGG_User| Lookup a board game geek user's game collection  | `!go *username*` |
| GetHotGames | Returns BoardGameGeeks current hot games | `!ghg` |
| GetHotCompanies | Returns BoardGameGeeks current hot board game companies | `!ghc` |



## Support on Beerpay
Hey dude! Help me out for a couple of :beers:!

[![Beerpay](https://beerpay.io/matta174/BoardGameBot/badge.svg?style=beer-square)](https://beerpay.io/matta174/BoardGameBot)  [![Beerpay](https://beerpay.io/matta174/BoardGameBot/make-wish.svg?style=flat-square)](https://beerpay.io/matta174/BoardGameBot?focus=wish)
