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
import youtube_dl
import Python.BGG


from threading import Timer
from discord import Game
from discord.ext.commands import Bot, CommandNotFound
from Python.YouTube import how_to_play, game_ambiance, search_next_video
from Python.DataStorage import getScore, getStartTime, setStartTime,\
     getEndTime, addPoint, addUser
from Python.Dice import dice
from util.config import TOKEN
from util.database_initialization import intitialize_db


if not os.path.isfile('boardgamebot.db'):
    intitialize_db()

Bot_Prefix = ("?", "!")

players = {}

client = Bot(command_prefix=Bot_Prefix)


@client.command(name='BGGCheck',
                description="Returns the BGG information on a game",
                brief="Returns the Board Game Geek information of a game",
                aliases=['bggck', 'bglookup', 'bg']
                )
async def BGGCheck(ctx, *, gamename):
    main_response = game_lookup(gamename)
    await ctx.send(main_response)


@client.command(name='Expansion_Check',
                description="Returns expansions for the selected game if any",
                brief="Returns expansions of a game",
                aliases=['exp', 'expchk', 'expansion']
                ) 
async def Expansion_Check(ctx, *, game):
    main_response = game_expansion(game)
    await ctx.send(main_response)


@client.command(name='Random_Game',
                description="Returns a random game title from a provided list",
                brief="Returns a random title from a provided list of games",
                aliases=['randompick', 'randbg', 'rbg']
                )
async def random_game(ctx, *, arg):
    possible_responses = arg.split(',')
    await ctx.send(random.choice(possible_responses))


@client.command(name='Random_Owned_Game',
                description="Returns a random game title from a user's owned \
                    list",
                brief="Returns a random title from a user's owned list of \
                    games",
                aliases=['randomownedpick', 'randobg', 'robg']
                )
async def random_users_game(ctx, name):
    random_game_name = random_owned_game(name)
    await ctx.send(random_game_name)


@client.command(name='What_Game_Can_We_Play',
                description="Looks up a user's collection and how many people are playing to see what games you could play",
                brief="Looks up a user's collection and how many people are playing to see what games you could play",
                aliases=['wgcwp', 'wcwp', 'whatcanweplay']
                )
async def what_game_can_we_play(ctx, *, arg):
    userInput = arg.split(',')
    name = userInput[0]
    number_of_players = int(userInput[1])
    games_we_can_play = what_games_can_we_play(name, number_of_players)
    await ctx.send(games_we_can_play)    


@client.command(name='Playtime_Timer',
                description="Sets the start of a play time timer",
                brief="Times playtime of a game",
                aliases=['starttimer', 'timerstart', 'st']
                )
async def Playtime_Timer(ctx):
    setStartTime()
    await ctx.send(
        "Started the timer at: " +
        str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))


@client.command(name='End_Time',
                description="Checks the elapsed time since the start of the \
                    timer",
                brief="Stops the timer",
                aliases=['endtimer', 'end_time', 'et']
                )
async def end_time(ctx):
    end_time = getEndTime()
    await ctx.send("Total play time: " + end_time)


@client.command(name='Check_Score',
                description="Checks the user's score",
                brief="Checks user's scores",
                aliases=['chksc', 'check_score', 'cs']
                )
async def check_score(ctx):
    scores = getScore()
    await ctx.send("Total wins per user: " + str(scores))


@client.command(name='Add_Point',
                description="Adds a point to the user's score",
                brief="Adds a point to the user's score",
                aliases=['addpt', 'add_point', 'ap']
                )
async def add_point(ctx, user):
    addPoint(user)
    await ctx.send("Added point to " + user)


@client.command(name='HowToPlay',
                description="Returns the top search result video from YouTube \
                    on how to play",
                brief="How to play video",
                aliases=['htp', 'how', 'video']
                )
async def youtube_how_to(ctx, *,gamename):
    main_response = how_to_play(gamename)
    await ctx.send(main_response)


@client.command()
async def schedule(ctx, date):
    timenow = datetime.datetime.now()
    await ctx.say(str(timenow))

@client.command(name='GetHotGames',
                description="Returns BoardGameGeeks current hot games",
                brief="Returns BoardGameGeeks current hot games",
                aliases=['ghg', 'gethotgames']
                )
async def gethotgames(ctx):
    response = hot_games()
    await ctx.send(response)


@client.command(name='GetHotCompanies',
                description="Returns BoardGameGeeks current hot board game companies",
                brief="Returns BoardGameGeeks current hot board game companies",
                aliases=['ghc', 'gethotcompanies']
                )
async def gethotcompanies(ctx):
    response = hot_companies()
    await ctx.send(response)


@client.command(name='AskQuestion',
                description="Returns a search of Stack Exchange similar questions",
                brief="Returns a search of Stack Exchange similar questions",
                aliases=['ask', 'ASK', 'question']
                )
async def ask(ctx, *, arg):
    userInput = arg.split(',')
    game = userInput[0]
    question = userInput[1]
    response = search_stackexchange(game, question)
    await ctx.send(response)


@client.command(name='Lookup_BGG_User',
                description='Lookup BGG user',
                brief="lookup bgg user",
                aliases=['gamesowned', 'lookup-games', 'go']
                )
async def lookup_bgg_user(ctx, name):
    response = user_lookup(name)
    await ctx.send("Games that " + name + " owns: \n" + response)


@client.command(name="Dice_Roll",
                description="Returns the value of a dice roll number is specified by command",
                brief="Returns the value of a dice roll",
                aliases=['dice']
                )
async def dice_roll(ctx, sides):
    dice_roll = dice(int(sides))
    await ctx.send("The " + str(sides) + " sided die resulted in: " + str(dice_roll))               


@client.command(name='Game_Ambiance',
                description="Returns the top search result video from YouTube",
                brief="Ambiance video",
                aliases=['amb', 'ambiance']
                )
async def game_ambiance_playlist(ctx, *, topic):
    main_response = game_ambiance(topic)
    await ctx.send("Here's the result for " + topic +
                   " ambiance \n" + main_response)


@client.command(name='Next_Video',
                description="Returns the next video in the last youtube search",
                brief="Return next video",
                aliases=['nextvid', 'nxt', 'nvideo']
                )
async def next_video(ctx):
    response = search_next_video()
    await ctx.send("Next video: \n" + response)


@client.event
async def on_command_error(error, ctx):
    if isinstance(error, CommandNotFound):
        return await ctx.send(ctx.message.channel,
                                         '\"' + ctx.invoked_with + '\"'
                                         ' is not a valid ' +
                                         ' command. Please try again.' +
                                         ' Use !help <command name> to get ' +
                                         'more info on how to use a ' +
                                         'specific command.')
    raise error


@client.event
async def on_ready():
    print('Ready!')


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed():
        print("Current servers:")
        for guild in client.guilds:
            print(guild.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
