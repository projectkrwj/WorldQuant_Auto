import sqlite3

conn = sqlite3.connect("worldquant.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM fields
    LIMIT 10
""")

for row in cursor.fetchall():
    print(dict(row))

conn.close()