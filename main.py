# Work with Python 3.6
import asyncio
import datetime
import logging
import os
import random
import typing

import discord.ext.commands
import Python.BGG
import Python.data_storage
import Python.Dice
import Python.YouTube
import sentry_sdk
import util.database_initialization
from util.config import TOKEN
from util.config import sentry_url

if not os.path.isfile('boardgamebot.db'):
    util.database_initialization.intitialize_db()

sentry_sdk.init(sentry_url)

logger = logging.Logger('catch_all')

Bot_Prefix = ("?", "!")

players = {}

client = discord.ext.commands.Bot(command_prefix=Bot_Prefix)


@client.command(name='BGGCheck',
                description="Returns the BGG information on a game",
                brief="Returns the Board Game Geek information of a game",
                aliases=['bggck', 'bglookup', 'bg']
                )
async def bgg_check(ctx, *, gamename):
    main_response = Python.BGG.game_lookup(gamename)
    filepath = Python.BGG.image_lookup(gamename)
    embed = discord.Embed()
    embed.set_image(url=filepath)
    await ctx.send(main_response,embed=embed)


@client.command(name='Expansion_Check',
                description="Returns expansions for the selected game if any",
                brief="Returns expansions of a game",
                aliases=['exp', 'expchk', 'expansion']
                ) 
async def expansion_check(ctx, *, game):
    main_response = Python.BGG.game_expansion(game)
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
    random_game_name = Python.BGG.random_owned_game(name)
    await ctx.send(random_game_name)


@client.command(name='What_Game_Can_We_Play',
                description="Looks up a user's collection and how many people are playing to see what games you could play",
                brief="Looks up a user's collection and how many people are playing to see what games you could play",
                aliases=['wgcwp', 'wcwp', 'whatcanweplay']
                )
async def what_game_can_we_play(ctx, *, arg):
    user_input = arg.split(',')
    name = user_input[0]
    number_of_players = int(user_input[1])
    games_we_can_play = Python.BGG.what_games_can_we_play(name, number_of_players)
    await ctx.send(games_we_can_play)


@client.command(name='Get_All_Wins',
                description="Gets the wins of every user for every game",
                brief="Checks user's scores",
                aliases=['getwins', 'get_wins', 'gw']
                )
async def get_all_wins(ctx, member: typing.Optional[discord.Member] = None, *, arg=None):
    response = Python.data_storage.get_wins(ctx, member, arg)
    await ctx.send(response)


@get_all_wins.error
async def get_all_wins_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error retrieving wins, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Add_Win',
                description="Adds a win to the user's total for a game",
                brief="Adds a win to ther user for a game",
                aliases=['addwin', 'add_win', 'aw', 'win'],
                )
async def add_win(ctx, member: discord.Member, *, game_name):
    response = Python.data_storage.add_win_db(ctx, member, game_name)
    await ctx.send(response)


@add_win.error
async def add_win_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send('Failed to add win. Make sure you are using the format `!aw [user] [boardgame name]`'
                       ' and that you are mentioning the user directly with @.')
        logger.error(error, exc_info=True)
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send('Failed to add win as you did not provide either the user who won or the name of the game. '
                       'Make sure you are using the format `!aw [user] [boardgame name]`'
                       ' and that you are mentioning the user directly with @.')
        logger.error(error, exc_info=True)
    elif isinstance(error, BaseException):
        await ctx.send('Unexpected error adding win, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Add_Game',
                description="Adds a game to the database so wins can be recorded for it",
                brief="Adds a game to the database",
                aliases=['addgame', 'add_game', 'ag'],
                )
async def add_game(ctx, *, name):
    response = Python.data_storage.add_game_db(ctx, name)
    await ctx.send(response)

@add_game.error
async def add_game_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error adding game, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')


@client.command(name='Add_Play',
                description="Logs a play to a game in the database",
                brief="Logs a play",
                aliases=['addplay', 'add_play', 'ap'],
                )
async def add_play(ctx, *, name):
    response = Python.data_storage.add_play_db(ctx, name)
    await ctx.send(response)


@add_play.error
async def add_play_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected adding play, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')

@client.command(name='Get_Plays',
                description="Gets all plays either for one game or for all games",
                brief="Gets all plays",
                aliases=['getplays', 'get_plays', 'gp'],
                )
async def get_plays_db(ctx, *, name=None):
    response = Python.data_storage.get_plays_db(ctx, name)
    await ctx.send(response)

@get_plays_db.error
async def get_plays_db_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error retrieving plays, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')


@client.command(name='HowToPlay',
                description="Returns the top search result video from YouTube \
                    on how to play",
                brief="How to play video",
                aliases=['htp', 'how', 'video']
                )
async def youtube_how_to(ctx, *, game_name):
    main_response = Python.YouTube.how_to_play(game_name)
    await ctx.send(main_response)


@client.command()
async def schedule(ctx):
    time_now = datetime.datetime.now()
    await ctx.say(str(time_now))


@client.command(name='GetHotGames',
                description="Returns BoardGameGeeks current hot games",
                brief="Returns BoardGameGeeks current hot games",
                aliases=['ghg', 'gethotgames']
                )
async def get_hot_games(ctx):
    response = Python.BGG.hot_games()
    await ctx.send(response)


@client.command(name='GetHotCompanies',
                description="Returns BoardGameGeeks current hot board game companies",
                brief="Returns BoardGameGeeks current hot board game companies",
                aliases=['ghc', 'gethotcompanies']
                )
async def get_hot_companies(ctx):
    response = Python.BGG.hot_companies()
    await ctx.send(response)


@client.command(name='AskQuestion',
                description="Returns a search of Stack Exchange similar questions",
                brief="Returns a search of Stack Exchange similar questions",
                aliases=['ask', 'ASK', 'question']
                )
async def ask(ctx, *, arg):
    user_input = arg.split(',')
    game = user_input[0]
    question = user_input[1]
    response = Python.BGG.search_stackexchange(game, question)
    await ctx.send(response)


@client.command(name='Lookup_BGG_User',
                description='Lookup BGG user',
                brief="lookup bgg user",
                aliases=['gamesowned', 'lookup-games', 'go']
                )
async def lookup_bgg_user(ctx, name):
    response = Python.BGG.user_lookup(name)
    await ctx.send("Games that " + name + " owns: \n" + response)


@client.command(name="Dice_Roll",
                description="Returns the value of a dice roll number is specified by command",
                brief="Returns the value of a dice roll",
                aliases=['dice']
                )
async def dice_roll(ctx, sides):
    dice_roll = Python.Dice.dice(int(sides))
    await ctx.send("The " + str(sides) + " sided die resulted in: " + str(dice_roll))               


@client.command(name='Game_Ambiance',
                description="Returns the top search result video from YouTube",
                brief="Ambiance video",
                aliases=['amb', 'ambiance']
                )
async def game_ambiance_playlist(ctx, *, topic):
    main_response = Python.YouTube.game_ambiance(topic)
    await ctx.send("Here's the result for " + topic +
                   " ambiance \n" + main_response)


@client.command(name='Next_Video',
                description="Returns the next video in the last youtube search",
                brief="Return next video",
                aliases=['nextvid', 'nxt', 'nvideo']
                )
async def next_video(ctx):
    response = Python.YouTube.search_next_video()
    await ctx.send("Next video: \n" + response)


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
