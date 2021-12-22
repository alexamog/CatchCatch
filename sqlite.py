import sqlite3

conn = sqlite3.connect("characters.db")
c = conn.cursor()

c.execute("""INSERT INTO characters VALUES (Frankun, 100, False, 'None') """)
conn.commit()

# test = c.fetchall()
# print(test)

conn.close()