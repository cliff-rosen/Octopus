import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from src.config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.connection.autocommit = True

    def __del__(self):
        if self.connection.is_connected():
            self.connection.close()

    def execute(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.lastrowid
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    # User Management
    def create_user(self, username, password):
        password_hash = generate_password_hash(password)
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        return self.execute(query, (username, password_hash))

    def authenticate_user(self, username, password):
        query = "SELECT id, password_hash FROM users WHERE username = %s"
        result = self.execute(query, (username,))
        if result and check_password_hash(result[0]['password_hash'], password):
            return result[0]['id']
        return None

    # Session Management
    def create_session(self, user_id):
        session_token = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=24)
        query = "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (%s, %s, %s)"
        self.execute(query, (user_id, session_token, expires_at))
        return session_token

    def validate_session(self, session_token):
        query = "SELECT user_id FROM sessions WHERE session_token = %s AND expires_at > NOW()"
        result = self.execute(query, (session_token,))
        return result[0]['user_id'] if result else None

    def invalidate_session(self, session_token):
        query = "DELETE FROM sessions WHERE session_token = %s"
        self.execute(query, (session_token,))

    # Virtual Screen Management
    def create_screen(self, user_id, name):
        url = f"/screens/{str(uuid.uuid4())}"
        query = "INSERT INTO virtual_screens (user_id, name, url) VALUES (%s, %s, %s)"
        screen_id = self.execute(query, (user_id, name, url))
        return {"id": screen_id, "name": name, "url": url}

    def get_user_screens(self, user_id):
        query = "SELECT id, name, url FROM virtual_screens WHERE user_id = %s"
        return self.execute(query, (user_id,))

    def get_screen(self, screen_id, user_id):
        query = "SELECT id, name, url FROM virtual_screens WHERE id = %s AND user_id = %s"
        result = self.execute(query, (screen_id, user_id))
        return result[0] if result else None

    def update_screen(self, screen_id, user_id, name):
        query = "UPDATE virtual_screens SET name = %s, updated_at = NOW() WHERE id = %s AND user_id = %s"
        self.execute(query, (name, screen_id, user_id))
        return self.get_screen(screen_id, user_id)

    def delete_screen(self, screen_id, user_id):
        query = "DELETE FROM virtual_screens WHERE id = %s AND user_id = %s"
        self.execute(query, (screen_id, user_id))

    # Additional methods for content management can be added here
    # For example:
    # def get_screen_content(self, screen_id):
    #     ...
    # def update_screen_content(self, screen_id, content):
    #     ...

# Usage example:
# db = Database()