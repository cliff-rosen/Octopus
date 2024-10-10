import unittest
from src.db.database import Database
from src.config import DB_CONFIG
import mysql.connector

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test database
        cls.test_db_name = 'test_octopus'
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.test_db_name}")
        connection.close()

        # Update DB_CONFIG to use the test database
        cls.original_db_name = DB_CONFIG['database']
        DB_CONFIG['database'] = cls.test_db_name

        # Create necessary tables
        cls.db = Database()
        cls.db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        ''')
        cls.db.execute('''
            CREATE TABLE IF NOT EXISTS virtual_screens (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        cls.db.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                session_token VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL
            )
        ''')

    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        # cursor.execute(f"DROP DATABASE IF EXISTS {cls.test_db_name}")
        connection.close()

        # Restore original DB_CONFIG
        DB_CONFIG['database'] = cls.original_db_name

    def setUp(self):
        self.db = Database()

    def tearDown(self):
        # Clear all tables after each test
        
        #self.db.execute("DELETE FROM sessions")
        #self.db.execute("DELETE FROM virtual_screens")
        #self.db.execute("DELETE FROM users")
        pass

    def test_create_and_authenticate_user(self):
        user_id = self.db.create_user("testuser", "testpassword")
        self.assertIsNotNone(user_id)

        authenticated_id = self.db.authenticate_user("testuser", "testpassword")
        self.assertEqual(user_id, authenticated_id)

        wrong_auth_id = self.db.authenticate_user("testuser", "wrongpassword")
        self.assertIsNone(wrong_auth_id)

    def test_session_management(self):
        user_id = self.db.create_user("sessionuser", "sessionpass")
        session_token = self.db.create_session(user_id)
        self.assertIsNotNone(session_token)

        validated_user_id = self.db.validate_session(session_token)
        self.assertEqual(user_id, validated_user_id)

        self.db.invalidate_session(session_token)
        invalid_user_id = self.db.validate_session(session_token)
        self.assertIsNone(invalid_user_id)

    def test_virtual_screen_management(self):
        user_id = self.db.create_user("screenuser", "screenpass")
        
        # Create screen
        screen = self.db.create_screen(user_id, "Test Screen")
        self.assertIsNotNone(screen['id'])
        self.assertEqual(screen['name'], "Test Screen")

        # Get user screens
        screens = self.db.get_user_screens(user_id)
        self.assertEqual(len(screens), 1)
        self.assertEqual(screens[0]['name'], "Test Screen")

        # Update screen
        updated_screen = self.db.update_screen(screen['id'], user_id, "Updated Screen")
        self.assertEqual(updated_screen['name'], "Updated Screen")

        # Get specific screen
        fetched_screen = self.db.get_screen(screen['id'], user_id)
        self.assertEqual(fetched_screen['name'], "Updated Screen")

        # Delete screen
        self.db.delete_screen(screen['id'], user_id)
        deleted_screen = self.db.get_screen(screen['id'], user_id)
        self.assertIsNone(deleted_screen)

if __name__ == '__main__':
    unittest.main()