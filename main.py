# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import datetime
import traceback
import logging
import pprint
from threading import Timer
from discord import Game
from discord.ext.commands import Bot
from Python.BGG import game_lookup
from Python.YouTube import how_to_play
from Python.DataStorage import getScore, getStartTime, setStartTime, getEndTime, addPoint, addUser


Bot_Prefix = ("?", "!")
TOKEN = 'NTUyNTEwMjkzNzA0NzA0MDAy.D2AlXA.6c9dXthL89p4tnCbV40G1_elbCo'

client = Bot(command_prefix=Bot_Prefix)


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command(name='BGGCheck',
                description="Returns the BGG information on a game",
                brief="From the world of board gaming",
                aliases=['bggck', 'bglookup', 'bg']
                )
async def BGGCheck(gamename):
    main_response = game_lookup(gamename)
    await client.say(main_response)


@client.command(name='Random_Game',
                description="Returns a random game title from a provided list",
                brief="From the world of board gaming",
                aliases=['randompick', 'randbg', 'rbg'],
                pass_context=True
                )
async def random_game(ctx, *, arg):
    possible_responses = arg.split(',')
    await client.say(random.choice(possible_responses))


@client.command(name='Playtime_Timer',
                description="Sets the start of a play time timer",
                brief="Times playtime of a game",
                aliases=['starttimer', 'timerstart', 'st'],
                pass_context=True
                )
async def Playtime_Timer():
    setStartTime()
    await client.say("Started the timer at: " + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))


@client.command(name='End_Time',
                description="Checks the elapsed time since the start of the timer",
                brief="Stops the timer",
                aliases=['endtimer', 'end_time', 'et'],
                pass_context=True)
async def end_time():
    end_time = getEndTime()
    await client.say("Total play time: " + end_time)


@client.command(name='Check_Score',
                description="Checks the user's score",
                brief="Checks user's scores",
                aliases=['chksc', 'check_score', 'cs'],
                pass_context=True)
async def check_score():
    scores = getScore()
    await client.say("Total wins per user: " + str(scores))


@client.command(name='Add_Point',
                description="Adds a point to the user's score",
                brief="Checks user's scores",
                aliases=['addpt', 'add_point', 'ap'],
                )
async def add_point(user):
    addPoint(user)
    await client.say("Added point to " + user)

@client.command(name='HowToPlay',
                    description="Returns the top search result video from YouTube on how to play",
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

@client.command(name='Add_user',
                description="Adds a user",
                brief="Creates a user with 0 points",
                aliases=['addus','add_user','au'],
                )
async def add_user(name):
   addUser(name)
   await client.say("Added " + name)     


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)
