import sqlite3

conn = sqlite3.connect('management.db')

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL,
               email TEXT NOT NULL
            )''')

conn.commit()

cur.close()
conn.close()
