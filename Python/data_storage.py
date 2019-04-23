import sqlite3
import logging
import prettytable

logger = logging.Logger('catch_all')


def get_wins(ctx, member, arg):
    try:
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        response = None
        if member and arg:
            c.execute('SELECT g.name, discord_id, number_of_wins ' +
                      'FROM wins ' +
                      'INNER JOIN games g on wins.game_id = g.id ' +
                      'WHERE discord_id = ' + str(member.id) +
                      ' AND g.name = ' + '\'' + arg + '\'' +
                      ' AND server_id = ' + str(ctx.guild.id) +
                      ' GROUP BY g.name, discord_id')
            response = prettify_wins_data(ctx, c)
        elif member:
            c.execute('SELECT g.name, discord_id, number_of_wins ' +
                      'FROM wins ' +
                      'INNER JOIN games g on wins.game_id = g.id ' +
                      'WHERE discord_id = ' + str(member.id) +
                      ' AND server_id = ' + str(ctx.guild.id) +
                      ' GROUP BY g.name, discord_id')
            response = prettify_wins_data(ctx, c)
        elif arg:
            c.execute('SELECT g.name, discord_id, number_of_wins ' +
                      'FROM wins ' +
                      'INNER JOIN games g on wins.game_id = g.id ' +
                      'WHERE g.name = ' + '\'' + arg + '\' ' +
                      'AND server_id = ' + str(ctx.guild.id) +
                      'GROUP BY g.name, discord_id')
            response = prettify_wins_data(ctx, c)
        else:
            c.execute('SELECT g.name, discord_id, number_of_wins ' +
                      'FROM wins ' +
                      'INNER JOIN games g on wins.game_id = g.id ' +
                      'WHERE server_id = ' + str(ctx.guild.id) +
                      'GROUP BY g.name, discord_id')
            response = prettify_wins_data(ctx, c)

    except BaseException as e:
        logger.error(e, exc_info=True)
        response = 'Failed to retrieve wins'
    finally:
        conn.close()
        return response


def add_win_db(ctx, member, arg):
    try:
        member_id = str(member.id)
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('SELECT id FROM games WHERE name = ? AND server_id = ?', (arg, str(ctx.guild.id,)))
        game_id = c.fetchone()
        if game_id:
            game_id = game_id[0]
            c.execute('SELECT id ' +
                      'FROM wins WHERE game_id = ?' +
                      ' AND server_id = ?' +
                      ' AND discord_id = ?', (game_id, str(ctx.guild.id), str(member_id),))
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
                response = 'Added a win to ' + member.name + ' for ' + arg
            else:
                c.execute("""INSERT INTO wins
                              (discord_id, game_id, number_of_wins, server_id)
                              VALUES (?,?,?,?)""", (member_id, game_id, 1, str(ctx.guild.id),))
                conn.commit()
            response = 'Added a win to ' + member.name + ' for ' + arg
        else:
            response = 'No game with the name ' + arg + ' could be found. Please add it first using the !ag command.'
    except BaseException as e:
        logger.error(e, exc_info=True)
        response = 'Failed to add a win to ' + member.name + ' for ' + arg
    finally:
        conn.close()
        return response


def add_game_db(ctx, name):
    try:
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('INSERT INTO games (name, server_id) VALUES (?,?)', (name, str(ctx.guild.id),))
        conn.commit()
        response = 'Added the game ' + name
    except sqlite3.IntegrityError as e:
        logger.error(e, exc_info=True)
        response = name + ' has already been added.'
    except BaseException as e:
        logger.error(e, exc_info=True)
        response = 'Failed to add game ' + name
    finally:
        return response
        conn.close()


def add_play_db(ctx, name):
    try:
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('SELECT id ' +
                  'FROM games ' +
                  'WHERE name = ? AND server_id = ?', (name, str(ctx.guild.id),))
        game_id = c.fetchone()
        if game_id:
            game_id = game_id[0]
            c.execute('SELECT number_of_plays FROM games ' +
                      'WHERE id = ? AND server_id = ?', (game_id, str(ctx.guild.id),))
            old_number_of_plays = c.fetchone()[0]
            c.execute('UPDATE games SET (number_of_plays) = ?' +
                      'WHERE id = ? AND server_id = ?', (old_number_of_plays + 1, game_id, str(ctx.guild.id)))
            conn.commit()
            if old_number_of_plays > 0:
                response = 'Logged play for \'' + name + '\'. You have played this game ' \
                           + str(old_number_of_plays + 1) + ' times.'
            else:
                response = 'Logged play for \'' + name + '\'. You have played this game one time'
        else:
            response = 'No game called \'' + name + '\' was found. Please add it first using the !ag command.'
    except BaseException as e:
        logger.error(e, exc_info=True)
        response = 'Failed to log a play for the game ' + name
    finally:
        conn.close()
        return response


def get_plays_db(ctx, name):
    if name:
        try:
            conn = sqlite3.connect('boardgamebot.db')
            c = conn.cursor()
            c.execute('SELECT name, number_of_plays FROM games WHERE name = ? AND server_id = ?', (name, str(ctx.guild.id),))
            conn.commit()
            game_plays = c.fetchone()

            if game_plays:
                pretty_table = prettytable.PrettyTable()
                pretty_table.field_names = ['Game', 'Plays']
                pretty_table.add_row([game_plays[0], str(game_plays[1])])

                response = '```' + pretty_table.get_string() + '```'
            else:
                response = 'No game called ' + name + ' was found. Please add it first using the !ag command.'

        except BaseException as e:
            logger.error(e, exc_info=True)
            response = 'Failed to retrieve plays for the game ' + name
        finally:
            conn.close()
            return response
    else:
        try:
            conn = sqlite3.connect('boardgamebot.db')
            c = conn.cursor()
            c.execute('SELECT name, number_of_plays FROM games WHERE server_id = ?', (str(ctx.guild.id),))
            conn.commit()
            game_plays = c.fetchall()

            pretty_table = prettytable.PrettyTable()
            pretty_table.field_names = ['Game', 'Plays']

            for game_play in game_plays:
                pretty_table.add_row([game_play[0], str(game_play[1])])

            response = '```' + pretty_table.get_string() + '```'
        except BaseException as e:
            logger.error(e, exc_info=True)
            response = 'Failed to retrieve plays'
        finally:
            conn.close()
            return response


def prettify_wins_data(ctx, cursor):
    rows = cursor
    if rows is None:
        return 'No wins found'
    else:
        pretty_table = prettytable.PrettyTable()
        pretty_table.field_names = ['Game', 'Player', 'Wins']

        for row in rows:
            pretty_table.add_row([row[0], ctx.guild.get_member(int(row[1])).display_name, row[2]])

        return '```' + pretty_table.get_string() + '```'
