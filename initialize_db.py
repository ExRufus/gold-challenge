# migrations/initialize_db.py

import sqlite3

def init_db():
    conn = sqlite3.connect('cleansed_data.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cleaned_texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_text TEXT NOT NULL,
        cleaned_text TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
