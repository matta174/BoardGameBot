import boardgamegeek
import random

bgg = boardgamegeek.BGGClient()


def game_lookup(string):
    game = bgg.game(string)
    rating = str( round(game.rating_average, 2))
    description = str(game.description.strip()[0:1000] + "...")
    gamerank = str(game.boardgame_rank)
    categories = game.categories
    number_of_players = str(game.min_players) + "-" + str(game.max_players)
    weight = str( round(game.rating_average_weight,2))
    categories_list = ', '.join(categories)
    return ("Game Rating for " + str(string) + " is: " + rating +
            "\nBoardGameGeek Rank: " + gamerank + "\nNumber of players: " +
            number_of_players + "\nCategories: " +
            categories_list + "\nComplexity Rank: " + weight +
            '/5' + "\n\nDescription: " + description)


def user_lookup(name):
    user = bgg.collection(name)
    games_string = ""
    for item in user.items:
        if item.owned:
            games_string = games_string + item.name + '\n'
    return(games_string)


def random_owned_game(name):
    user = bgg.collection(name)
    games_list = []
    for item in user.items:
        if item.owned:
            games_list.append(item.name)
    random_game = random.choice(games_list)
    return(random_game)

def what_games_can_we_play(name, numberofplayers = 1):
        user = bgg.collection(name)
        gamesString = ""
        for item in user.items:
                if item.owned:
                        if numberofplayers >= item.min_players and numberofplayers <= item.max_players:
                                gamesString = gamesString + item.name + '\n'
        return("With "+ str(numberofplayers) + " players you can play these games from " + name + "'s collection\n" + gamesString)


def hot_games():
        hot_games_list = bgg.hot_items('boardgame')
        returned_string = "The current hot games are: \n"
        for item in hot_games_list:
                returned_string = returned_string + item.name + '\n'
        return returned_string

