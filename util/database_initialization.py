def intitialize_db():
    import sqlite3

    conn = sqlite3.connect('boardgamebot.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS games (
                Game_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name text NOT NULL,
                Number_of_plays INTEGER DEFAULT 0,
                Total_play_time INTEGER DEFAULT 0
                )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS players (
                Player_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name text NOT NULL
                )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS wins (
                Wins_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Game_ID INTEGER,
                Name_ID INTEGER,
                Wins INTEGER DEFAULT 0,
                FOREIGN KEY(Game_ID) REFERENCES games(Game_ID),
                FOREIGN KEY(Name_ID) REFERENCES players(Name_ID)
                )""")

    conn.commit()
    conn.close()
