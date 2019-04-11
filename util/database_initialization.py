def intitialize_db():
    import sqlite3

    conn = sqlite3.connect('boardgamebot.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS games (
                name text NOT NULL UNIQUE PRIMARY KEY,
                number_of_plays INTEGER DEFAULT 0,
                total_play_time INTEGER DEFAULT 0
                )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS players (
                name text NOT NULL UNIQUE PRIMARY KEY
                )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS wins (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                game text NOT NULL,
                name text NOT NULL,
                wins INTEGER DEFAULT 0,
                FOREIGN KEY(game) REFERENCES games(name),
                FOREIGN KEY(name) REFERENCES players(name)
                )""")

    conn.commit()
    conn.close()
