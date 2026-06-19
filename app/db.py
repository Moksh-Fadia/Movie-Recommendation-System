import sqlite3
from datetime import datetime

DB_PATH = "app/search_history.db"  # sqlite file/path that will store the searches

# Create database/table
def init_db():      
    conn = sqlite3.connect(DB_PATH)   # connects to the sqlite database (creates the file if it doesn't exist)
    cursor = conn.cursor()     # creates a cursor object to execute SQL commands
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()   # saves (commits) the changes
    conn.close()    # closes the connection


# Insert search entry to the database
def add_search(title):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO search_history (title, timestamp) VALUES (?, ?)
    """, (title, datetime.now().strftime("%b %d, %Y %H:%M")))    # converting datetime object to simple form; %b = month abbrev, %d = day of month, %Y = year with century, %H = hour, %M = minute 
    conn.commit()
    conn.close()


# Fetch recent search history 
def get_recent_searches(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, timestamp FROM search_history ORDER BY id DESC LIMIT ?    
    """, (limit,))   
# order by id desc: sort results by the id column in descending order ie. latest searches first; limit means only return the top limit rows; ? is a placeholder for the limit parameter
# cursor.execute() requires parameters to be passed as a tuple even if there is only one parameter thats why we do (limit,) [a tuple with one item] and not (limit) [int]
    results = cursor.fetchall()     # returns all results as a list of tuples; eg: [("Inception", "2025-09-29T20:45:00"), ("Avengers", "2025-09-29T20:40:00")]
    conn.close()
    return results



