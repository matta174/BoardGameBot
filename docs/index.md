---
layout: page
title: BoardGameBot
tagline: Enhance your Discord Server with BoardGameBot
description: Easy to setup boardgame themed Discord bot.
---
# BoardGameBot

[![star this repo](http://githubbadges.com/star.svg?user=matta174&repo=BoardGameBot&style=default)](https://github.com/matta174/BoardGameBot)   [![fork this repo](http://githubbadges.com/fork.svg?user=matta174&repo=BoardGameBot&style=default)](https://github.com/matta174/BoardGameBot/fork)  [![Python 3.6.7](https://img.shields.io/badge/python-3.6.7-blue.svg)](https://www.python.org/downloads/release/python-360/)  ![GitHub repo size](https://img.shields.io/github/repo-size/matta174/boardgamebot.svg)    ![Discord](https://img.shields.io/discord/288694246721191947.svg)   ![GitHub issues](https://img.shields.io/github/issues-raw/matta174/boardgamebot.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/matta174/boardgamebot/badge)](https://www.codefactor.io/repository/github/matta174/boardgamebot)

BoardGameBot is a bot that can be used to quickly lookup information about board games as well as get how to play videos and much more.

## Prerequisites

### What items to install

discord - [link](https://github.com/Rapptz/discord.py)

boardgamegeek - [link](https://github.com/lcosmin/boardgamegeek)

Google APIs Client Library for Python - [link](https://developers.google.com/api-client-library/python/start/installation)

### How to install them

>pip install -U discord.py
>pip install boardgamegeek2
>pip install google-api-python-client
>pip install python-env
>pip install psycopg2
---

## Using the bot

* Create a new Discord Application [here](https://discordapp.com/developers/applications/)

* After creating the app on the app details page scroll down to the Bot page and create a bot.

* Save the token for the bot

* Go to this url https://discordapp.com/oauth2/authorize?client_id=XXXXXXXXXXXX&scope=bot and replace the client id with your app's client ID and authorize your app

* replace the token in main.py with your token and run

---

## Commands

| Name        | Description           | Command  |
| :-------------: |:-------------:| :-----:|
| Board Game Check      | Returns the BoardGameGeek.com  information of a specified game. | !bg *game name* |
| Expansion Check| Returns any expansions a game has if any. | !exp *game name* |
| Random Game     | Returns a random game title from a provided list of games separated by a comma.   |   !rbg *game name*, *game name* |
| Random Owned Game | Returns a random game title from a user's owned list.  | !robg *username*|
| What Game Can We Play | Looks up a specified user's game collection and how many people are playing to see what games you could play |!wcwp *username*, *number of players*|
| How To Play | Returns the top search result video from YouTube on how to play |  !htp *game name* |
| Next Video | Returns the next video in the last youtube search | !nxt |
| Ask | Returns a search of board gaming Stack Exchange similar questions.  |!ask *game name*,*question* |
| Dice Roll | Returns the value of a dice roll, side number is specified by command. | !dice *# of sides* |
| Game Ambiance | Returns the top search result video for selected topic from YouTube | !amb *topic* |
| Expansion Check | Returns expansions for the selected game if they exist | !exp *game name* |
| Lookup BGG User| Lookup a board game geek user's game collection  | !go *username* |
| Get Hot Games | Returns BoardGameGeeks current hot games | !ghg |
| Get Hot Companies | Returns BoardGameGeeks current hot board game companies | !ghc |

## Support the project on Beerpay

Hey! Buy us a  :beers:!

[![Beerpay](https://beerpay.io/matta174/BoardGameBot/badge.svg?style=beer-square)](https://beerpay.io/matta174/BoardGameBot)  [![Beerpay](https://beerpay.io/matta174/BoardGameBot/make-wish.svg?style=flat-square)](https://beerpay.io/matta174/BoardGameBot?focus=wish)

---

### Contributors

* [Cody Stallings](https://github.com/ydocsgnillats)
* [Josh Nicholson](https://github.com/joshua-nicholson)
* [Matthew Compton](https://github.com/matta174)