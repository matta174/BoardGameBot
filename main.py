# Work with Python 3.6
import asyncio
import random
import json
import datetime
import traceback
import logging
import pprint
import xml.etree.ElementTree
import requests
import time
import os

from threading import Timer
from discord import Game
from discord import Member
from discord.ext.commands import Bot, CommandNotFound
from Python.BGG import game_lookup, user_lookup, random_owned_game
from Python.YouTube import how_to_play, game_ambiance
from Python.DataStorage import getScore, getStartTime, setStartTime,\
     getEndTime, addWin
from util.config import TOKEN
from util.database_initialization import intitialize_db


if not os.path.isfile('boardgamebot.db'):
    intitialize_db()

Bot_Prefix = ("?", "!")

client = Bot(command_prefix=Bot_Prefix)


@client.command(name='BGGCheck',
                description="Returns the BGG information on a game",
                brief="Returns the Board Game Geek information of a game",
                aliases=['bggck', 'bglookup', 'bg']
                )
async def BGGCheck(gamename):
    main_response = game_lookup(gamename)
    await client.say(main_response)


@client.command(name='Random_Game',
                description="Returns a random game title from a provided list",
                brief="Returns a random title from a provided list of games",
                aliases=['randompick', 'randbg', 'rbg'],
                pass_context=True
                )
async def random_game(ctx, *, arg):
    possible_responses = arg.split(',')
    await client.say(random.choice(possible_responses))


@client.command(name='Random_Owned_Game',
                description="Returns a random game title from a user's owned \
                    list",
                brief="Returns a random title from a user's owned list of \
                    games",
                aliases=['randomownedpick', 'randobg', 'robg']
                )
async def random_users_game(name):
    random_game_name = random_owned_game(name)
    await client.say(random_game_name)


@client.command(name='Playtime_Timer',
                description="Sets the start of a play time timer",
                brief="Times playtime of a game",
                aliases=['starttimer', 'timerstart', 'st'],
                pass_context=True
                )
async def Playtime_Timer():
    setStartTime()
    await client.say(
        "Started the timer at: " +
        str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))


@client.command(name='End_Time',
                description="Checks the elapsed time since the start of the \
                    timer",
                brief="Stops the timer",
                aliases=['endtimer', 'end_time', 'et'],
                pass_context=True)
async def end_time():
    end_time = getEndTime()
    await client.say("Total play time: " + end_time)
    await client.change_presence


@client.command(name='Check_Score',
                description="Checks the user's score",
                brief="Checks user's scores",
                aliases=['chksc', 'check_score', 'cs'],
                pass_context=True)
async def check_score():
    scores = getScore()
    await client.say("Total wins per user: " + str(scores))


@client.command(name='Add_Win',
                description="Adds a win to the user's total for a game",
                brief="Adds a win to ther user for a game",
                aliases=['addwin', 'add_win', 'aw', 'win'],
                )
async def add_win(ctx, member: discord.Member, arg):
    response = addWin(arg)
    await client.say(response)


@client.command(name='HowToPlay',
                description="Returns the top search result video from YouTube \
                    on how to play",
                brief="How to play video",
                aliases=['htp', 'how', 'video']
                )
async def youtube_how_to(gamename):
    main_response = how_to_play(gamename)
    await client.say(main_response)


@client.command()
async def schedule(date):
    timenow = datetime.datetime.now()
    await client.say(str(timenow))


@client.command(name='Lookup_BGG_User',
                description='Lookup BGG user',
                brief="lookup bgg user",
                aliases=['gamesowned', 'lookup-games', 'go'])
async def lookup_bgg_user(name):
    response = user_lookup(name)
    await client.say("Games that " + name + " owns: \n" + response)


@client.command(name='Game_Ambiance',
                description="Returns the top search result video from YouTube",
                brief="Ambiance video",
                aliases=['amb', 'ambiance']
                )
async def game_ambiance_playlist(topic):
    main_response = game_ambiance(topic)
    await client.say("Here's the result for " + topic +
                     " ambiance \n" + main_response)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.event
async def on_command_error(error, ctx):
    if isinstance(error, CommandNotFound):
        return await client.send_message(ctx.message.channel,
                                         '\"' + ctx.invoked_with + '\"'
                                         ' is not a valid ' +
                                         ' command. Please try again.' +
                                         ' Use !help <command name> to get ' +
                                         'more info on how to use a ' +
                                         'specific command.')
    raise error

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
