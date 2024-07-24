# app/utils/modification.py

import sqlite3

# Function to save cleansed data to the database
def save_to_db(original_text, cleaned_text):
    conn = sqlite3.connect('cleansed_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO cleaned_texts (original_text, cleaned_text)
    VALUES (?, ?)
    ''', (original_text, cleaned_text))
    conn.commit()
    conn.close()

# Function to get all processed texts from the database
def get_all_processed_texts():
    conn = sqlite3.connect('cleansed_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_text, cleaned_text FROM cleaned_texts')
    rows = cursor.fetchall()
    conn.close()
    texts = [{"original": row[0], "processed": row[1]} for row in rows]
    return texts
