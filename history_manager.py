import sqlite3
from datetime import datetime

class HistoryManager:
    
    def __init__(self, db_path="history.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id TEXT,
            file_name TEXT NOT NULL, 
            from_path TEXT NOT NULL, 
            to_path TEXT NOT NULL, 
            moved_at TEXT NOT NULL
        );
        """
        
        self.conn.execute(query)
        self.conn.commit()
    
    def add_record(self, batch_id, file_name, from_path, to_path):
        query = """
        INSERT INTO history (batch_id, file_name, from_path, to_path, moved_at)
        VALUES (?, ?, ?, ?, ?)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(query, (batch_id, file_name, from_path, to_path, timestamp))
        self.conn.commit()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            
    def get_history(self, limit=None):
        """
        Read move history from the database,
        Returns list of dict:
        [
            {"id": 1, "batch_id": "...", "file_name": "...", ...},
            ...
        ]
        """
        
        cursor = self.conn.cursor()
        
        if limit is None:
            cursor.execute("SELECT id, batch_id, file_name, from_path, to_path, moved_at FROM history ORDER BY id DESC")
        else:
            cursor.execute(
                "SELECT id, batch_id, file_name, from_path, to_path, moved_at FROM history ORDER BY id DESC LIMIT ?",
                (limit,)
            )
        
        rows = cursor.fetchall()
        
        columns = ["id", "batch_id", "file_name", "from_path", "to_path", "moved_at"]
        
        result = []
        for row in rows:
            row_dict = {columns[i]: row[i] for i in range(len(columns))}
            result.append(row_dict)
            
        return result
    
    def delete_all_history(self):
        """Delete all history records"""
        query = "DELETE FROM history"
        self.conn.execute(query)
        self.conn.commit()