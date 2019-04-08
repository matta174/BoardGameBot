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


from threading import Timer
from discord import Game
from discord.ext.commands import Bot, CommandNotFound
from Python.BGG import game_lookup, user_lookup, random_owned_game, what_games_can_we_play, hot_games, hot_companies, game_expansion
from Python.YouTube import how_to_play, game_ambiance, search_next_video
from Python.DataStorage import getScore, getStartTime, setStartTime,\
     getEndTime, addPoint, addUser
from util.config import TOKEN

Bot_Prefix = ("?", "!")

players = {}

client = Bot(command_prefix=Bot_Prefix)

@client.command(name='BGGCheck',
                description="Returns the BGG information on a game",
                brief="Returns the Board Game Geek information of a game",
                aliases=['bggck', 'bglookup', 'bg'],
                pass_context=True
                )
async def BGGCheck(ctx,*, gamename):
    main_response = game_lookup(gamename)
    await client.say(main_response)


@client.command(name= 'Expansion_Check',
                description = "Returns expansions for the selected game if they exist",
                brief = "Returns expansions of a game",
                aliases = ['exp', 'expchk', 'expansion'],
                pass_context = True
                ) 
async def Expansion_Check(ctx,*, game):
    main_response = game_expansion(game)
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


@client.command(name='What_Game_Can_We_Play',
                description="Looks up a user's collection and how many people are playing to see what games you could play",
                brief="Looks up a user's collection and how many people are playing to see what games you could play",
                aliases=['wgcwp','wcwp','whatcanweplay'],
                pass_context = True
                )
async def what_game_can_we_play(ctx, *, arg):
    userInput = arg.split(',')
    name = userInput[0]
    number_of_players = int(userInput[1])
    games_we_can_play = what_games_can_we_play(name, number_of_players)
    await client.say(games_we_can_play)    


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


@client.command(name='Add_Point',
                description="Adds a point to the user's score",
                brief="Adds a point to the user's score",
                aliases=['addpt', 'add_point', 'ap'],
                )
async def add_point(user):
    addPoint(user)
    await client.say("Added point to " + user)


@client.command(name='HowToPlay',
                description="Returns the top search result video from YouTube \
                    on how to play",
                brief="How to play video",
                aliases=['htp', 'how', 'video'], 
                pass_context=True
                )
async def youtube_how_to(ctx, *,gamename):
    main_response = how_to_play(gamename)
    await client.say(main_response)


@client.command()
async def schedule(date):
    timenow = datetime.datetime.now()
    await client.say(str(timenow))

@client.command(name = 'GetHotGames',
                description = "Returns BoardGameGeeks current hot games",
                brief="Returns BoardGameGeeks current hot games",
                aliases=['ghg','gethotgames']
                )
async def gethotgames():
    response = hot_games()
    await client.say(response)

@client.command(name = 'GetHotCompanies',
                description = "Returns BoardGameGeeks current hot board game companies",
                brief="Returns BoardGameGeeks current hot board game companies",
                aliases=['ghc','gethotcompanies']
                )
async def gethotcompanies():
    response = hot_companies()
    await client.say(response)



@client.command(name='Add_user',
                description="Adds a user",
                brief="Creates a user with 0 points",
                aliases=['addus', 'add_user', 'au'],
                )
async def add_user(name):
    addUser(name)
    await client.say("Added " + name)


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
                aliases=['amb', 'ambiance'],
                pass_context = True
                )
async def game_ambiance_playlist(ctx, *,topic):
    main_response = game_ambiance(topic)
    await client.say("Here's the result for " + topic +
                     " ambiance \n" + main_response)


@client.command(name = 'Next_Video',
                description = "Returns the next video in the last youtube search",
                brief = "Return next video",
                aliases = ['nextvid', 'nxt', 'nvideo'])
async def next_video():
    response = search_next_video()
    await client.say("Next video: \n" + response)


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



@client.command(pass_context=True)
async def AmbianceAudio(ctx, topic):
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    voice_client = client.voice_client_in(server)
    url = game_ambiance(topic)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id 
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id 
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id 
    players[id].resume()    

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
