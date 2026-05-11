import sqlite3
import os
from data_access.db_config import DB_PATH, DATA_DIR, USERS_CSV, BOOKS_CSV, RENTALS_CSV, USER_FIELDS, BOOK_FIELDS, RENTAL_FIELDS
from data_access.csv_handler import CSVHandler

class DBHandler:

    @staticmethod
    def get_connection():
        os.makedirs(DATA_DIR, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def setup_tables():
        conn = DBHandler.get_connection()
        cur = conn.cursor()

        print("[SQL] Creating tables...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id  TEXT PRIMARY KEY,
                name     TEXT NOT NULL,
                password TEXT NOT NULL,
                role     TEXT NOT NULL,
                status   TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id   TEXT PRIMARY KEY,
                title     TEXT NOT NULL,
                writer    TEXT NOT NULL,
                category  TEXT NOT NULL,
                book_type TEXT NOT NULL,
                available TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                rental_id   TEXT PRIMARY KEY,
                user_id     TEXT NOT NULL,
                book_id     TEXT NOT NULL,
                issue_date  TEXT NOT NULL,
                due_date    TEXT NOT NULL,
                return_date TEXT
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("[SQL] Tables created successfully\n")

    @staticmethod
    def load(table):
        conn = DBHandler.get_connection()
        query = f"SELECT * FROM {table}"
        print(f"\n[SQL] {query}")
        cur = conn.execute(query)
        rows = [dict(r) for r in cur.fetchall()]
        print(f"[RESULT] {len(rows)} rows found\n")
        conn.close()
        return rows

    @staticmethod
    def find_one(table, key, value):
        conn = DBHandler.get_connection()
        query = f"SELECT * FROM {table} WHERE {key} = '{value}'"
        print(f"\n[SQL] {query}")
        cur = conn.execute(
            f"SELECT * FROM {table} WHERE {key} = ?", (value,)
        )
        row = cur.fetchone()
        if row:
            print(f"[RESULT] 1 row found\n")
        else:
            print(f"[RESULT] No rows found\n")
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def insert(table, data):
        conn = DBHandler.get_connection()
        keys = ", ".join(data.keys())
        vals = ", ".join([f"'{v}'" for v in data.values()])
        query = f"INSERT INTO {table} ({keys}) VALUES ({vals})"
        print(f"\n[SQL] {query}")
        
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO {table} ({keys}) VALUES ({', '.join(['?'] * len(data))})",
            list(data.values())
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[RESULT] Row inserted successfully\n")
        
        # CSV mein bhi save kar
        if table == "users":
            CSVHandler.append_row(USERS_CSV, data, USER_FIELDS)
        elif table == "books":
            CSVHandler.append_row(BOOKS_CSV, data, BOOK_FIELDS)
        elif table == "rentals":
            CSVHandler.append_row(RENTALS_CSV, data, RENTAL_FIELDS)

    @staticmethod
    def update(table, key, value, updated_data):
        conn = DBHandler.get_connection()
        sets = ", ".join([f"{k} = '{v}'" for k, v in updated_data.items()])
        query = f"UPDATE {table} SET {sets} WHERE {key} = '{value}'"
        print(f"\n[SQL] {query}")
        
        cur = conn.cursor()
        cur.execute(
            f"UPDATE {table} SET {', '.join([f'{k} = ?' for k in updated_data])} WHERE {key} = ?",
            list(updated_data.values()) + [value]
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[RESULT] Row updated successfully\n")
        
        # Poora table reload aur CSV mein save
        all_rows = DBHandler.load(table)
        if table == "users":
            CSVHandler.save(USERS_CSV, all_rows, USER_FIELDS)
        elif table == "books":
            CSVHandler.save(BOOKS_CSV, all_rows, BOOK_FIELDS)
        elif table == "rentals":
            CSVHandler.save(RENTALS_CSV, all_rows, RENTAL_FIELDS)

    @staticmethod
    def delete(table, key, value):
        conn = DBHandler.get_connection()
        query = f"DELETE FROM {table} WHERE {key} = '{value}'"
        print(f"\n[SQL] {query}")
        
        cur = conn.cursor()
        cur.execute(
            f"DELETE FROM {table} WHERE {key} = ?", (value,)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[RESULT] Row deleted successfully\n")
        
        # Poora table reload aur CSV mein save
        all_rows = DBHandler.load(table)
        if table == "users":
            CSVHandler.save(USERS_CSV, all_rows, USER_FIELDS)
        elif table == "books":
            CSVHandler.save(BOOKS_CSV, all_rows, BOOK_FIELDS)
        elif table == "rentals":
            CSVHandler.save(RENTALS_CSV, all_rows, RENTAL_FIELDS)

    @staticmethod
    def save(table, all_data):
        conn = DBHandler.get_connection()
        query = f"DELETE FROM {table}"
        print(f"\n[SQL] {query}")
        cur = conn.cursor()
        cur.execute(query)
        
        if all_data:
            keys = ", ".join(all_data[0].keys())
            print(f"[SQL] INSERT INTO {table} ({keys}) VALUES (...) x {len(all_data)}")
            
            for row in all_data:
                cur.execute(
                    f"INSERT INTO {table} ({keys}) VALUES ({', '.join(['?'] * len(row))})",
                    list(row.values())
                )
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"[RESULT] {len(all_data)} rows saved successfully\n")
        
        
        if table == "users":
            CSVHandler.save(USERS_CSV, all_data, USER_FIELDS)
        elif table == "books":
            CSVHandler.save(BOOKS_CSV, all_data, BOOK_FIELDS)
        elif table == "rentals":
            CSVHandler.save(RENTALS_CSV, all_data, RENTAL_FIELDS)