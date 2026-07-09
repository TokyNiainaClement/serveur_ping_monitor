import threading
import time

from views.fenetre import PingMonitorDarkApp
from data.database import Database
from core.ping_service import ping


class DashboardController:
    """
    Contrôleur : orchestre le ping en arrière-plan et la fenêtre Tkinter.
    Les machines et les événements proviennent maintenant de la base SQLite
    (data/ping_monitor.db) au lieu d'une liste codée en dur.
    """

    def __init__(self):
        self.db = Database()
        self.intervalle = 5  # secondes entre chaque cycle de ping

        # 1. On construit la fenêtre (ne bloque plus, grâce à run() séparé)
        self.view = PingMonitorDarkApp()

        # 2. self.view existe déjà : le thread peut l'utiliser en sécurité
        self._start_ping_thread()

        # 3. Fermeture propre de la connexion SQLite quand on ferme la fenêtre
        self.view.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # 4. On lance réellement l'affichage (bloque ici jusqu'à fermeture)
        self.view.run()

    # ------------------------------------------------------------------
    # PARTIE PING (lit les machines depuis la BDD)
    # ------------------------------------------------------------------

    def _boucle_ping(self):
        """Boucle infinie : ping toutes les machines de la BDD, toutes les X secondes."""
        while True:
            machines = self.db.get_machines()  # [(id, nom, ip), ...]

            for id_m, nom, ip in machines:
                en_ligne = ping(ip)
                statut = "En ligne" if en_ligne else "Hors ligne"
                heure = time.strftime("%H:%M:%S")

                # Écriture en base (thread de ping, aucun widget touché ici)
                self.db.add_evenement(ip, nom, statut)

                # ⚠️ Mise à jour de l'UI toujours via after() sur le thread principal
                self.view.root.after(0, self._mettre_a_jour_vue, heure, nom, statut)

            time.sleep(self.intervalle)

    def _mettre_a_jour_vue(self, heure, nom, statut):
        """
        Exécutée sur le thread principal (via after()).
        C'est ICI, et seulement ici, qu'on a le droit de modifier
        les widgets Tkinter.
        """
        self.view.ajouter_evenement(heure, nom, statut)

    def _start_ping_thread(self):
        """Démarre la boucle de ping dans un thread séparé."""
        thread = threading.Thread(target=self._boucle_ping, daemon=True)
        thread.start()

    def _on_close(self):
        """Ferme proprement la connexion SQLite avant de quitter."""
        self.db.close()
        self.view.root.destroy()
