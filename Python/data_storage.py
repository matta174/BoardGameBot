import sqlite3
import logging
import prettytable

logger = logging.Logger('catch_all')


def get_wins(ctx, member, game_name):
    conn = sqlite3.connect('boardgamebot.db')
    c = conn.cursor()
    if member and game_name:
        c.execute('SELECT g.name, discord_id, number_of_wins ' +
                  'FROM wins ' +
                  'INNER JOIN games g on wins.game_id = g.id ' +
                  'WHERE discord_id =  ? ' +
                  'AND g.name = ? ' +
                  'AND wins.server_id = ? ' +
                  'GROUP BY g.name, discord_id', (str(member.id), game_name, str(ctx.guild.id)), )
        response = prettify_wins_data(ctx, c)
    elif member:
        c.execute('SELECT g.name, discord_id, number_of_wins ' +
                  'FROM wins ' +
                  'INNER JOIN games g on wins.game_id = g.id ' +
                  'WHERE discord_id = ? ' +
                  'AND wins.server_id = ? ' +
                  'GROUP BY g.name, discord_id', (str(member.id), str(ctx.guild.id),))
        response = prettify_wins_data(ctx, c)
    elif game_name:
        c.execute('SELECT g.name, discord_id, number_of_wins ' +
                  'FROM wins ' +
                  'INNER JOIN games g on wins.game_id = g.id ' +
                  'WHERE g.name = ? ' +
                  'AND wins.server_id = ? ' +
                  'GROUP BY g.name, discord_id', (game_name, str(ctx.guild.id),))
        response = prettify_wins_data(ctx, c)
    else:
        c.execute('SELECT g.name, discord_id, number_of_wins ' +
                  'FROM wins ' +
                  'INNER JOIN games g on wins.game_id = g.id ' +
                  'WHERE wins.server_id = ? ' +
                  'GROUP BY g.name, discord_id', (str(ctx.guild.id),))
        response = prettify_wins_data(ctx, c)

    conn.close()
    return response


def add_win_db(ctx, member, game_name):
    member_id = str(member.id)
    conn = sqlite3.connect('boardgamebot.db')
    c = conn.cursor()
    c.execute('SELECT id FROM games WHERE name = ? AND server_id = ?', (game_name, str(ctx.guild.id, )))
    game_id = c.fetchone()

    if game_id:
        game_id = game_id[0]
        c.execute('SELECT id ' +
                  'FROM wins WHERE game_id = ?' +
                  ' AND wins.server_id = ?' +
                  ' AND discord_id = ?', (game_id, str(ctx.guild.id), str(member_id),))
        wins_id = c.fetchone()
        if wins_id:
            wins_id = wins_id[0]
            c.execute('SELECT number_of_wins FROM wins ' +
                      'WHERE id = ?', str(wins_id),)
            old_number_of_wins = c.fetchone()[0]
            c.execute('UPDATE wins SET number_of_wins = ? ' +
                      'WHERE id = ?',
                      (old_number_of_wins + 1, wins_id,))
            conn.commit()
            response = 'Added a win to ' + member.name + ' for ' + game_name
        else:
            c.execute("""INSERT INTO wins
                              (discord_id, game_id, number_of_wins, server_id)
                              VALUES (?,?,?,?)""", (member_id, game_id, 1, str(ctx.guild.id),))
            conn.commit()
            response = 'Added a win to ' + member.name + ' for ' + game_name
    else:
        response = 'No game with the name ' + game_name + ' could be found. Please add it first using the !ag command.'

    conn.close()
    return response


def add_game_db(ctx, name):
    conn = sqlite3.connect('boardgamebot.db')
    c = conn.cursor()
    rows = c.execute('SELECT id FROM games WHERE name = ? AND server_id = ?', (name, str(ctx.guild.id),))

    if not rows:
        c.execute('INSERT INTO games (name, server_id) VALUES (?,?)', (name, str(ctx.guild.id),))
        conn.commit()
        response = 'Added the game ' + name
    else:
        response = name + ' has already been added.'

    conn.close()
    return response


def add_play_db(ctx, name):
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

    conn.close()
    return response


def get_plays_db(ctx, name):
    if name:
        conn = sqlite3.connect('boardgamebot.db')
        c = conn.cursor()
        c.execute('SELECT name, number_of_plays FROM games WHERE name = ? AND server_id = ?',
                  (name, str(ctx.guild.id),))
        conn.commit()
        game_plays = c.fetchone()

        if game_plays:
            pretty_table = prettytable.PrettyTable()
            pretty_table.field_names = ['Game', 'Plays']
            pretty_table.add_row([game_plays[0], str(game_plays[1])])

            response = '```' + pretty_table.get_string() + '```'
        else:
            response = 'No game called ' + name + ' was found. Please add it first using the !ag command.'

        conn.close()
        return response
    else:
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
        conn.close()
        return response


def prettify_wins_data(ctx, cursor):
    rows = cursor.fetchall()
    if not rows:
        response = 'No wins found.'
    else:
        pretty_table = prettytable.PrettyTable()
        pretty_table.field_names = ['Game', 'Player', 'Wins']

        for row in rows:
            pretty_table.add_row([row[0], ctx.guild.get_member(int(row[1])).display_name, row[2]])

        response = '```' + pretty_table.get_string() + '```'

    return response
