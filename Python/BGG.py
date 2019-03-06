import boardgamegeek

bgg = boardgamegeek.BGGClient()


def game_lookup(string):
    game = bgg.game(string)
    rating = str(game.rating_average)
    description = str(game.description.strip()[0:1000] +"...")
    gamerank = str(game.boardgame_rank)
    categories = game.categories
    number_of_players = str(game.min_players) + "-" + str(game.max_players)
    weight = str(game.rating_average_weight)
    categories_list = ', '.join(categories)
    return ("Game Rating for " + str(string) + " is: " +  rating + "\nBoardGameGeek Rank: " + gamerank +"\nNumber of players: " + number_of_players + "\nCategories: " + categories_list  + "\nComplexity Rank: " + weight + '/5' + "\n\nDescription: " + description)
