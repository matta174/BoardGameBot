def intitialize_db():
    import sqlite3

    conn = sqlite3.connect('boardgamebot.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL COLLATE NOCASE,
                server_id text NOT NULL,
                number_of_plays INTEGER DEFAULT 0
                )""")

    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS wins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                number_of_wins INTEGER DEFAULT 0,
                discord_id text NOT NULL,
                server_id text NOT NULL,
                FOREIGN KEY(game_id) REFERENCES games(id) 
                )""")

    conn.commit()
    conn.close()
