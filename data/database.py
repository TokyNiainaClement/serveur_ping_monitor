import sqlite3
import os
from datetime import datetime

# Le fichier .db sera créé dans le dossier data/
DB_PATH = os.path.join(os.path.dirname(__file__), "ping_monitor.db")


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        # check_same_thread=False car le threading sera utilisé pour le dashboard Tkinter
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._creer_tables()

    def _creer_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS machines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                ip TEXT NOT NULL UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS evenements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                heure TEXT NOT NULL,
                ip TEXT NOT NULL,
                nom TEXT NOT NULL,
                evenement TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_machines(self):
        """Retourne la liste des machines enregistrées : [(id, nom, ip), ...]"""
        self.cursor.execute("SELECT id, nom, ip FROM machines")
        return self.cursor.fetchall()

    def add_evenement(self, ip, nom, evenement):
        heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO evenements (heure, ip, nom, evenement) VALUES (?, ?, ?, ?)",
            (heure, ip, nom, evenement),
        )
        self.conn.commit()

    def get_evenements(self, limit=50):
        self.cursor.execute(
            "SELECT id, heure, ip, nom, evenement FROM evenements ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
