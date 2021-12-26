import sqlite3

conn = sqlite3.connect("characters.db")
c = conn.cursor()

c.execute("""CREATE TABLE characters (
        char_name  TEXT,
        char_val INTEGER,
        char_owned TEXT,
        char_owner TEXT
        )""")

conn.commit() #Commits the table to the db file
conn.close() #Closes the connection