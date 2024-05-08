import sqlite3

def create_table_users():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100),
            password VARCHAR(100)
        )
    ''')
