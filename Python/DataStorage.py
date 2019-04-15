import json
import datetime
import time
import sqlite3
import logging

logger = logging.Logger('catch_all')


def getScore():
    jsonFile = open("data\\users.json", "r+")
    data = json.load(jsonFile)
    output_string = "\n"
    for d in data['users']:
        output_string += d['name'] + ': ' + str(d['score']) + '\n'
    return output_string


def addWin(ctx, member, arg):
    try:
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('SELECT id FROM games WHERE name = \'' + arg + '\'')
        game_id = c.fetchall()
        if game_id:
                c.execute('SELECT id ' +
                          'FROM wins WHERE game_id = \'' + game_id + '\'' +
                          'AND discord_id = \'' + member.id + '\'')
                wins_id = c.fetchall()
                if wins_id:
                    c.execute('SELECT number_of_wins FROM wins ' +
                              'WHERE wins_id = ' + wins_id + '\'')
                    old_number_of_wins = c.fetchall()
                    c.execute('UPDATE wins SET number_of_wins = ? ' +
                              'WHERE id = ?',
                              (old_number_of_wins + 1, wins_id,))
                    conn.commit()
                else:
                    c.execute('''INSERT INTO wins
                              (discord_id, game_id, number_of_wins)
                              VALUES (?,?,?)''', (member.id, game_id, 1))
                return 'Added a win to ' + user + ' for ' + game
        else:
            return """No game with the name ' + arg + ' could be found.
                      Please add it first using the !ag command."""
    except BaseException as e:
        logger.error(e, exc_info=true)
        return 'Failed to add a win to ' + user + ' for ' + game
    finally:
        conn.close()


def getStartTime():
    jsonFile = open("data\\playtime.json", "r+")
    data = json.load(jsonFile)
    return data["start time"]


def setStartTime():
    start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    with open("data\\playtime.json", "r+") as json_file:
        json_decoded = json.load(json_file)
    json_decoded["start time"] = start_time
    with open("data\\playtime.json", "r+") as json_file:
        json.dump(json_decoded, json_file)


def getEndTime():
    jsonFile = open("data\\playtime.json", "r+")
    data = json.load(jsonFile)
    string_date = data["start time"]
    formatted_datetime_object = datetime.datetime.strptime(
        string_date, '%Y-%m-%dT%H:%M:%S.%f')
    elapsed_time = datetime.datetime.now() - formatted_datetime_object
    return str(elapsed_time)
