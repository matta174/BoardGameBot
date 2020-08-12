# Work with Python 3.6
import asyncio
import datetime
import logging
import random

import discord.ext.commands

import Python.BGG
import Python.Dice
import Python.YouTube
import Python.data_storage
from util.config import TOKEN

# if not os.path.isfile('boardgamebot.db'):
#     util.database_initialization.intitialize_db()

# sentry_sdk.init(sentry_url)

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
    if "error" not in filepath:
        embed.set_image(url=filepath)
    if filepath == "error":
        await ctx.send(main_response)
        return
    await ctx.send(main_response, embed=embed)


@bgg_check.error
async def bgg_check_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Expansion_Check',
                description="Returns expansions for the selected game if any",
                brief="Returns expansions of a game",
                aliases=['exp', 'expchk', 'expansion']
                )
async def expansion_check(ctx, *, game):
    main_response = Python.BGG.game_expansion(game)
    await ctx.send(main_response)


@expansion_check.error
async def expansion_check_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Random_Game',
                description="Returns a random game title from a provided list",
                brief="Returns a random title from a provided list of games",
                aliases=['randompick', 'randbg', 'rbg']
                )
async def random_game(ctx, *, arg):
    possible_responses = arg.split(',')
    await ctx.send(random.choice(possible_responses))


@random_game.error
async def random_game_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


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


@random_users_game.error
async def random_users_game_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


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
    if games_we_can_play.__len__() > 2000:
        for chunk in [games_we_can_play[i:i + 2000] for i in range(0, len(games_we_can_play), 2000)]:
            await ctx.send(chunk + '\n')
        return
    await ctx.send(games_we_can_play)


@what_game_can_we_play.error
async def what_game_can_we_play_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='HowToPlay',
                description="Returns the top search result video from YouTube \
                    on how to play",
                brief="How to play video",
                aliases=['htp', 'how', 'video']
                )
async def youtube_how_to(ctx, *, game_name):
    main_response = Python.YouTube.how_to_play(game_name)
    await ctx.send(main_response)


@youtube_how_to.error
async def youtube_how_to_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command()
async def schedule(ctx):
    time_now = datetime.datetime.now()
    await ctx.say(str(time_now))


@client.command(name='GetHotGames',
                description="Returns BoardGameGeeks current hot games",
                brief="Returns BoardGameGeeks current hot games",
                aliases=['ghg', 'gethotgames', 'hot']
                )
async def get_hot_games(ctx):
    response = Python.BGG.hot_games()
    await ctx.send(response)


@get_hot_games.error
async def get_hot_games_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='GetHotCompanies',
                description="Returns BoardGameGeeks current hot board game companies",
                brief="Returns BoardGameGeeks current hot board game companies",
                aliases=['ghc', 'gethotcompanies']
                )
async def get_hot_companies(ctx):
    response = Python.BGG.hot_companies()
    await ctx.send(response)


@get_hot_companies.error
async def get_hot_companies_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


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


@ask.error
async def ask_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Lookup_BGG_User',
                description='Lookup BGG user',
                brief="lookup bgg user",
                aliases=['gamesowned', 'lookup-games', 'go']
                )
async def lookup_bgg_user(ctx, name):
    response = Python.BGG.user_lookup(name)
    await ctx.send("Games that " + name + " owns: \n\n" + response)


@lookup_bgg_user.error
async def lookup_bgg_user_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name="Dice_Roll",
                description="Returns the value of a dice roll number is specified by command",
                brief="Returns the value of a dice roll",
                aliases=['dice']
                )
async def dice_roll(ctx, sides):
    dice_roll = Python.Dice.dice(int(sides))
    await ctx.send("The " + str(sides) + " sided die resulted in: " + str(dice_roll))


@dice_roll.error
async def dice_roll_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Game_Ambiance',
                description="Returns the top search result video from YouTube",
                brief="Ambiance video",
                aliases=['amb', 'ambiance']
                )
async def game_ambiance_playlist(ctx, *, topic):
    main_response = Python.YouTube.game_ambiance(topic)
    await ctx.send("Here's the result for " + topic +
                   " ambiance \n" + main_response)


@game_ambiance_playlist.error
async def game_ambiance_playlist_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Next_Video',
                description="Returns the next video in the last youtube search",
                brief="Return next video",
                aliases=['nextvid', 'nxt', 'nvideo']
                )
async def next_video(ctx):
    response = Python.YouTube.search_next_video()
    await ctx.send("Next video: \n" + response)


@next_video.error
async def next_video_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.event
async def on_ready():
    print('Ready!')


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed():
        print("Current servers:")
        for guild in client.guilds:
            print(guild.name)
        await client.change_presence(activity=discord.Game(name=Python.BGG.random_owned_game("matta174")))
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)
