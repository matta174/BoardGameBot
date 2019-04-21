def intitialize_db():
    import sqlite3

    conn = sqlite3.connect('boardgamebot.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL UNIQUE COLLATE NOCASE,
                number_of_plays INTEGER DEFAULT 0
                )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS wins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                number_of_wins INTEGER DEFAULT 0,
                discord_id text,
                FOREIGN KEY(game_id) REFERENCES games(game_id) 
                )""")

    conn.commit()
    conn.close()
