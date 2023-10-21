import sqlite3
from datetime import datetime

def create_database(db_name='qa_database.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            date_added TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_qa(username, question, answer, db_name='qa_database.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO user_data (username, question, answer, date_added) VALUES (?, ?, ?, ?)', (username, question, answer, date_added))
    conn.commit()
    conn.close()

def get_qa(username, db_name='qa_database.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT question, answer, date_added FROM user_data WHERE username=?', (username,))
    data = cursor.fetchall()
    conn.close()
    return data
def showallqa(db_name="qa_database.db"):
   
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data ",)
    return cursor.fetchall()

def del_qa(username,db_name="qa_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_data WHERE username = ?",(username,))
    conn.commit()
    conn.close()
    if get_qa(username)==[]:
        return 'data deleted successfully'
    else:
        return 'failed to delete data'