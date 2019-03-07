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
from Python.DataStorage import getData, getStartTime, setStartTime, getEndTime


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
                aliases=['bggck','bglookup','bg']
                )    
async def BGGCheck(gamename):
    main_response = game_lookup(gamename)
    await client.say(main_response)   

@client.command(name='Random_Game',
                description="Returns a random game title from a provided list",
                brief="From the world of board gaming",
                aliases=['randompick','randbg','rbg'],
                pass_context = True
                )    
async def random_game(ctx, *, arg):
    possible_responses = arg.split(',')
    await client.say(random.choice(possible_responses))   


@client.command(name='Playtime_Timer',
                description="Sets the start of a play time timer",
                brief="Times playtime of a game",
                aliases=['starttimer','timerstart','st'],
                pass_context = True
                ) 
async def Playtime_Timer():
    setStartTime()
    await client.say("Started the timer at: " + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

@client.command(name='End_Time',
                description="Checks the elapsed time since the start of the timer",
                brief="Stops the timer",
                aliases=['endtimer','end_time','et'],
                pass_context = True)
async def end_time():
   end_time = getEndTime()
   await client.say("Total play time: " + end_time)

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