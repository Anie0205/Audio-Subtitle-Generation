import sqlite3

conn = sqlite3.connect("translations.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM translations")
for row in cursor.fetchall():
    print(row)
conn.close()
