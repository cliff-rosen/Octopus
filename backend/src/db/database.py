import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from config import DB_CONFIG

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
    def create_screen(self, user_id, name, content=""):
        url = f"/screens/{str(uuid.uuid4())}"
        query = "INSERT INTO virtual_screens (user_id, name, url, content) VALUES (%s, %s, %s, %s)"
        screen_id = self.execute(query, (user_id, name, url, content))
        return {"id": screen_id, "name": name, "url": url, "content": content}

    def get_user_screens(self, user_id):
        query = "SELECT id, name, url FROM virtual_screens WHERE user_id = %s"
        return self.execute(query, (user_id,))

    def get_screen(self, screen_id, user_id):
        query = "SELECT id, name, url, content FROM virtual_screens WHERE id = %s AND user_id = %s"
        result = self.execute(query, (screen_id, user_id))
        return result[0] if result else None

    def update_screen(self, screen_id, user_id, name=None, content=None):
        update_fields = []
        params = []
        if name is not None:
            update_fields.append("name = %s")
            params.append(name)
        if content is not None:
            update_fields.append("content = %s")
            params.append(content)
        
        if not update_fields:
            return None  # No updates to perform
        
        update_fields.append("updated_at = NOW()")
        query = f"UPDATE virtual_screens SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
        params.extend([screen_id, user_id])
        
        self.execute(query, tuple(params))
        return self.get_screen(screen_id, user_id)

    def delete_screen(self, screen_id, user_id):
        query = "DELETE FROM virtual_screens WHERE id = %s AND user_id = %s"
        self.execute(query, (screen_id, user_id))

    # Screen Content Management
    def get_screen_content(self, screen_id, user_id):
        query = "SELECT content FROM virtual_screens WHERE id = %s AND user_id = %s"
        result = self.execute(query, (screen_id, user_id))
        return result[0]['content'] if result else None

    def update_screen_content(self, screen_id, user_id, content):
        query = "UPDATE virtual_screens SET content = %s, updated_at = NOW() WHERE id = %s AND user_id = %s"
        self.execute(query, (content, screen_id, user_id))
        return self.get_screen(screen_id, user_id)

# Usage example:
# db = Database()