import sqlite3
import json
from models.user import User

class UserRepository:

    def __init__(self, db_path):
        self.db_path = db_path


    def create_user(self, username, password):
        """Insert a new user into the DB. Returns the created User object or None if fail."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, preferences) VALUES (?, ?, ?)",
                (username, password))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return User(user_id, username, password)
        except sqlite3.IntegrityError:
            return None


    def get_user_by_username(self, username):
        """Return a User object if the username exists, otherwise None."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username))
        row = cursor.fetchone()
        conn.close()
        if row:
            user_id, u_name, pwd = row
            return User(user_id, u_name, pwd)
        return None