from models.user import User
import psycopg2
from models.user import User


class UserRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_connection(self):
        """Establish a connection to the PostgreSQL database."""
        return psycopg2.connect(**self.db_config)

    def create_user(self, email, password):
        """Insert a new user into the DB. Returns the created User object or None if fail."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                (email, password)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return User(user_id, email, password)
        except psycopg2.IntegrityError:
            return None


    def get_user_by_username(self, username):
        """Return a User object if the username exists, otherwise None."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            user_id, u_name, pwd = row
            return User(user_id, u_name, pwd)
        return None