#SQLite조작하는 도구

import sqlite3


class Database:
    def __init__(self, db_name="worldquant.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets(
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            category_id TEXT,
            category_name TEXT,
            subcategory_id TEXT,
            subcategory_name TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS fields(
            id TEXT PRIMARY KEY, 
            dataset TEXT NOT NULL,
            region TEXT NOT NULL,
            type TEXT NOT NULL,
            category_id TEXT NOT NULL,
            category_name TEXT NOT NULL,
            description TEXT
        )
        """)

        self.conn.commit()

    def insert_datasets(self, rows):
        print("insert_datasets 호출:", len(rows))

        self.cursor.executemany("""
        INSERT OR REPLACE INTO datasets
        (id, name, description, category_id, category_name, subcategory_id, subcategory_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rows)

        self.conn.commit()

        self.cursor.execute("SELECT COUNT(*) FROM datasets")
        print("DB 내부 개수:", self.cursor.fetchone()[0])

    def insert_fields(self, rows):
        self.cursor.executemany("""
        INSERT OR REPLACE INTO fields
        (id, dataset, region, type, category_id, category_name, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rows)

        self.conn.commit()

    def close(self):
        self.conn.close()