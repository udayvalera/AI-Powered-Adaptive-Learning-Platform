import sqlite3
import json

class DBManager:
    def __init__(self, db_path='./db/roadmaps.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS roadmaps (
                    filename TEXT PRIMARY KEY,
                    roadmap_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quizzes (
                    filename TEXT,
                    node_id TEXT,
                    quiz_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (filename, node_id)
                )
            """)
            conn.commit()

    def store_roadmap(self, filename, roadmap_data):
        """Store a roadmap in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO roadmaps (filename, roadmap_data) VALUES (?, ?)",
                (filename, json.dumps(roadmap_data))
            )
            conn.commit()

    def get_roadmap(self, filename):
        """Retrieve a roadmap from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT roadmap_data FROM roadmaps WHERE filename = ?",
                (filename,)
            )
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
            return None
            
    def store_quiz(self, filename, node_id, quiz_data):
        """Store a quiz in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO quizzes (filename, node_id, quiz_data) VALUES (?, ?, ?)",
                (filename, node_id, json.dumps(quiz_data))
            )
            conn.commit()

    def get_quiz(self, filename, node_id):
        """Retrieve a quiz from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT quiz_data FROM quizzes WHERE filename = ? AND node_id = ?",
                (filename, node_id)
            )
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
            return None