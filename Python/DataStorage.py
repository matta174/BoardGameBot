import json
import datetime
import time
import sqlite3
import logging

logger = logging.Logger('catch_all')


def get_wins(ctx):
    try:
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('SELECT g.name, discord_id, number_of_wins ' + 
                     'FROM wins ' +
                     'INNER JOIN games g on wins.game_id = g.id ' +
                     'GROUP BY g.name, discord_id')
        rows = c.fetchall()
        response = ''

        for row in rows:
            response += row[0] + ' ' + ctx.guild.get_member(int(row[1])).display_name + ' ' + str(row[2]) + '\n'
            #TODO: Better formatting for this
        
        return response

    except BaseException as e:
            logger.error(e, exc_info=True)
            return 'Failed to retrieve wins'
    finally:
        conn.close()


def add_win_db(ctx, member, arg):
    try:
        member_id = str(member.id)
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('SELECT id FROM games WHERE name = \'' + arg + '\'')
        game_id = c.fetchone()
        if game_id:
                game_id = game_id[0]
                c.execute('SELECT id ' +
                          'FROM wins WHERE game_id = ' + str(game_id) +
                          ' AND discord_id = ' + member_id)
                wins_id = c.fetchone()
                if wins_id:
                    wins_id = wins_id[0]
                    c.execute('SELECT number_of_wins FROM wins ' +
                              'WHERE id = ' + str(wins_id))
                    old_number_of_wins = c.fetchone()[0]
                    c.execute('UPDATE wins SET number_of_wins = ? ' +
                              'WHERE id = ?',
                              (old_number_of_wins + 1, wins_id,))
                    conn.commit()
                    return 'Added a win to ' + member.name + ' for ' + arg
                else:
                    c.execute("""INSERT INTO wins
                              (discord_id, game_id, number_of_wins)
                              VALUES (?,?,?)""", (member_id, game_id, 1,))
                    conn.commit()
                return 'Added a win to ' + member.name + ' for ' + arg
        else:
            return 'No game with the name ' + arg + ' could be found. Please add it first using the !ag command.'
    except BaseException as e:
        logger.error(e, exc_info=True)
        return 'Failed to add a win to ' + member.name + ' for ' + arg
    finally:
        conn.close()


def add_game_db(ctx, name):
    try:
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('INSERT INTO games (name) VALUES (?)', (name,))
        conn.commit()
        return 'Added the game ' + name
    except sqlite3.IntegrityError as e:
        logger.error(e, exc_info=True)
        return name + ' has already been added.'
    except BaseException as e:
        logger.error(e, exc_info=True)
        return 'Failed to add game ' + name
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
