from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/spam_logs")
def get_spam_logs():
    """Fetch spam logs from database"""
    conn = sqlite3.connect("spam_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spam ORDER BY timestamp DESC LIMIT 50")
    logs = cursor.fetchall()
    conn.close()
    return {"spam_logs": logs}
