import sqlite3

conn = sqlite3.connect('cpm.db')

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL,
               email TEXT NOT NULL
            )''')

cur.execute("INSERT INTO users (username, email) VALUES (?, ?)", ('john_doe', 'john@example.com'))
cur.execute("INSERT INTO users (username, email) VALUES (?, ?)", ('jane_doe', 'jane@example.com'))

conn.commit()

cur.execute("SELECT * FROM users")
print("Users:")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
