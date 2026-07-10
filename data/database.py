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

    def add_machine(self, nom, ip):
        """Insère une nouvelle machine. Retourne True si succès, False si l'IP existe déjà."""
        try:
            self.cursor.execute(
                "INSERT INTO machines (nom, ip) VALUES (?, ?)",
                (nom, ip),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # L'IP existe déjà (contrainte UNIQUE)
            return False

    def add_evenement(self, ip, nom, evenement):
        heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO evenements (heure, ip, nom, evenement) VALUES (?, ?, ?, ?)",
            (heure, ip, nom, evenement),
        )
        self.conn.commit()

    def get_evenements(self, limit=50, ip=None):
        """
        Retourne l'historique des événements, du plus récent au plus ancien.
        Si `ip` est fourni, ne retourne que l'historique de cette machine.
        """
        if ip:
            self.cursor.execute(
                "SELECT id, heure, ip, nom, evenement FROM evenements "
                "WHERE ip = ? ORDER BY id DESC LIMIT ?",
                (ip, limit),
            )
        else:
            self.cursor.execute(
                "SELECT id, heure, ip, nom, evenement FROM evenements "
                "ORDER BY id DESC LIMIT ?",
                (limit,),
            )
        return self.cursor.fetchall()

    def update_machine(self, id_m, nom, ip):
        """Modifie le nom/l'IP d'une machine. Retourne True si succès, False si l'IP existe déjà ailleurs."""
        try:
            self.cursor.execute(
                "UPDATE machines SET nom = ?, ip = ? WHERE id = ?",
                (nom, ip, id_m),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_machine(self, id_m):
        """Supprime une machine de la liste surveillée (garde son historique d'événements)."""
        self.cursor.execute("DELETE FROM machines WHERE id = ?", (id_m,))
        self.conn.commit()

    def get_stats_globales(self):
        """Calcule la disponibilité (%) et le nombre de pannes sur tout l'historique."""
        self.cursor.execute(
            "SELECT COUNT(*) FROM evenements WHERE evenement = 'En ligne'"
        )
        en_ligne = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) FROM evenements WHERE evenement = 'Hors ligne'"
        )
        pannes = self.cursor.fetchone()[0]

        total = en_ligne + pannes
        disponibilite = (en_ligne / total * 100) if total > 0 else 0
        return disponibilite, pannes

    def close(self):
        self.conn.close()
