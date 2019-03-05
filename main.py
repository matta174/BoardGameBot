# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import datetime
from discord import Game
from discord.ext.commands import Bot
from Python.BGG import getRating
from Python.BGG import getDescription
from Python.BGG import getGameRank
from Python.BGG import getPublishers

Bot_Prefix = ("?","!")
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
                aliases=['bggck','bgscore','bg']
                )    
async def BGGCheck(gamename):
    # async with aiohttp.ClientSession() as session:  # Async HTTP request
        
        
        # raw_response = await session.get(url)
        # response = await raw_response.text()
        # response = json.loads(response)
        gameNameString = str(gamename)
        boardgame_rating = getRating(gameNameString)
        boardgame_description = getDescription(gameNameString)
        boardgame_rank = getGameRank(gameNameString)
        publishers = getPublishers(gameNameString)
        publisher_string = ""
        for p in publishers:
            publisher_string +=  p +" "

        

        main_response = "Game Rating " + str(gamename) + " is: " +  boardgame_rating + "\nBoardGameGeek Rank: " + boardgame_rank+ "\nPublishers: " + publisher_string  + "\n\n" + boardgame_description
        await client.say(main_response)   




@client.command()
async def schedule(date):
    timenow = datetime.datetime.now()
    await client.say(str(timenow) )

@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)