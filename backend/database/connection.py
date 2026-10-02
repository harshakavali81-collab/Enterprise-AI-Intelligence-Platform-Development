import os, sqlite3
from typing import Any, List, Dict, Optional

DATABASE_URL = os.getenv("DATABASE_URL", "")
LOCAL_SQLITE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/sample/enterprise_ai.db"))

class DatabaseConnection:
    """
    Database connection factory.
    Connects to PostgreSQL in container/cloud or local SQLite database for tests & dev.
    """
    @staticmethod
    def get_connection():
        # Connect in read-write or create mode
        conn = sqlite3.connect(LOCAL_SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def execute_query(sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        if cursor.description:
            cols = [col[0] for col in cursor.description]
            rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        else:
            rows = []
            conn.commit()
        conn.close()
        return rows
