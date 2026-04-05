import sqlite3
from datetime import datetime

db_name = "amadeus.db"

def init_db():
    with sqlite3.connect(db_name) as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS users 
            (user_id INTEGER PRIMARY KEY, persona TEXT, daily_count INTEGER, 
            last_reset TEXT, history TEXT)
            '''
        )

def get_user(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(db_name, timeout=10)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    user = cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    
    if not user:
        default_p = "You are (Makise Kurisu), genius, tsundere, cool person, smart" # kinda weird but yeah 😭

        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?)", 
            (user_id, default_p, 0, today, '[]')
        )

        conn.commit()
        user = cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    
    user_dict = dict(user)

    if user_dict['last_reset'] != today:
        cursor.execute("UPDATE users SET daily_count = 0, last_reset = ? WHERE user_id = ?", (today, user_id))
        conn.commit()
        user_dict['daily_count'] = 0
    
    conn.close()
    return user_dict

def update_user(user_id, **kwargs):
    query = "UPDATE users SET " + ", ".join([f"{k}=?" for k in kwargs.keys()]) + " WHERE user_id=?"
    values = list(kwargs.values()) + [user_id]
    with sqlite3.connect(db_name) as conn:
        conn.execute(query, values)

# you got a star ⭐
