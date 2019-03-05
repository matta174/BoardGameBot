import boardgamegeek

bgg = boardgamegeek.BGGClient()

def getRating(string):
    game = bgg.game(string)
    returned_string = str(game.rating_average)
    return (returned_string)


def getDescription(string):
    game = bgg.game(string)
    returned_string = str(game.description.strip()[0:1000] +"...")
    return (returned_string)   

def getGameRank(string):
    game = bgg.game(string)
    returned_string = str(game.boardgame_rank)
    return (returned_string)

def getPublishers(string):
    game = bgg.game(string)
    return (game.publishers)
# game = bgg.game("Android: Netrunner")
# print(game.boardgame_rank)
