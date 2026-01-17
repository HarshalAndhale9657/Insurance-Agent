import sqlite3
import json
import os
from typing import Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "../../sessions.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Initialize the sessions table if it doesn't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            user_id TEXT PRIMARY KEY,
            step TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_session(user_id: str) -> Dict[str, Any]:
    """
    Retrieve session data for a user. Returns a default session if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT step, data FROM sessions WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "step": row[0],
            "data": json.loads(row[1])
        }
    else:
        # Default new session
        return {"step": "welcome", "data": {}}

def update_session(user_id: str, step: str, data: Dict[str, Any]):
    """
    Update or insert session data for a user.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO sessions (user_id, step, data)
        VALUES (?, ?, ?)
    """, (user_id, step, json.dumps(data)))
    conn.commit()
    conn.close()

def get_all_sessions() -> list[Dict[str, Any]]:
    """
    Retrieve all sessions for the admin dashboard.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, step, data FROM sessions")
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "user_id": row[0],
            "step": row[1],
            "data": json.loads(row[2])
        })
    return results
