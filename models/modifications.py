# Import SQLite3
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
