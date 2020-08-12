import boardgamegeek
import random
import stackexchange

bgg = boardgamegeek.BGGClient()

so = stackexchange.Site(stackexchange.BoardampCardGames)


def game_lookup(string):
    try:
        game = bgg.game(string, choose="first")
    except Exception as e:
        return "Game not found, are you sure that's the correct title? Check for any possible errors."
    heart_count = int(game.rating_average)
    heart_emoji = '\U0001F49A'
    sad_heart_emoji = '\U0001F5A4'
    heart_string = heart_emoji
    for x in range(1, heart_count):
        heart_string += heart_emoji
    empty_heart_count = 10 - heart_count
    for x in range(0, empty_heart_count):
        heart_string += sad_heart_emoji
    heart_string += " (" + str(int(game.rating_average)) + " / 10)"

    description = str(game.description.strip()[0:1000] + "...")
    gamerank = str(game.boardgame_rank)
    categories = game.categories
    number_of_players = str(game.min_players) + "-" + str(game.max_players)
    weight = str(round(game.rating_average_weight, 2))
    categories_list = ', '.join(categories)
    return ("Game Rating for " + str(string) + " is: " + heart_string +
            "\nBoardGameGeek Rank: " + gamerank + "\nNumber of players: " +
            number_of_players + "\nCategories: " +
            categories_list + "\nComplexity Rank: " + weight +
            '/5' + "\nExpected game length: " + str(game.min_playing_time) + ' - ' + str(game.max_playing_time) +
            " Minutes" + "\n\nDescription: " + description)


def image_lookup(string):
    try:
        game = bgg.game(string, choose="best-rank")
    except Exception as e:
        return "error"
    return str(game.image)


def game_expansion(string):
    try:
        game = bgg.game(string)
    except Exception as e:
        return "Game not found, are you sure that's the correct title? Check for any possible errors."
    returned_string = "Here are the expansions for " + string + ":\n"
    expansion = game.expansions
    if not expansion:
        return "There are no expansions for " + str(game.name)
    for item in expansion:
        returned_string = returned_string + item.name + '\n'
    return returned_string


def user_lookup(name):
    try:
        user = bgg.collection(name)
    except Exception as e:
        return "User not found, are you sure that's the correct username? Check for any possible errors."
    games_string = ""
    for item in user.items:
        if item.owned:
            games_string = games_string + item.name + '\n'
    return (games_string)


def random_owned_game(name):
    try:
        user = bgg.collection(name)
    except Exception as e:
        return "User not found, are you sure that's the correct username? Check for any possible errors."
    games_list = []
    for item in user.items:
        if item.owned:
            games_list.append(item.name)
    random_game = random.choice(games_list)
    return random_game


def what_games_can_we_play(name, numberofplayers=1):
    try:
        user = bgg.collection(name)
    except Exception as e:
        return "User not found, are you sure that's the correct username? Check for any possible errors."
    games_string = ""
    for item in user.items:
        if item.owned:
            if item.min_players <= numberofplayers <= item.max_players:
                games_string = games_string + item.name + ' - Average Playtime:  ' + str(
                    item.playing_time) + ' minutes ' + '\n\n'

    return ("With " + str(
        numberofplayers) + " players you can play these games from " + name + "'s collection \n\n" + games_string)


def hot_games():
    hot_games_list = bgg.hot_items('boardgame')
    returned_string = "The current hot games are: \n\n"
    for item in hot_games_list:
        returned_string = returned_string + item.name + '\n'
    return returned_string


def hot_companies():
    hot_companies_list = bgg.hot_items('boardgamecompany')
    returned_string = "The current hot board game companies are: \n"
    for item in hot_companies_list:
        returned_string = returned_string + item.name + '\n'
    return returned_string


def search_stackexchange(game_tag, question):
    qs = so.similar(tagged=game_tag, title=question)
    returned_string = 'Here are the questions I found on the boardgames stack exchange: \n'
    limit = 0
    if qs:
        for q in qs:
            returned_string += str(q.link)
            if q.is_answered:
                returned_string += ' \U00002705'
            else:
                returned_string += ' \U0000274C'
            returned_string += '\n'
            limit += 1
            if limit == 5:
                break
    else:
        returned_string = 'No similar questions have been found on https://boardgames.stackexchange.com/'

    return returned_string

