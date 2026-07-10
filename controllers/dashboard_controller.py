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
        self.derniers_statuts = {}
        self.historique_dispo = []  # points % de disponibilité pour le graphique

        # 1. On construit la fenêtre (ne bloque plus, grâce à run() séparé)
        self.view = PingMonitorDarkApp(
            on_ajouter=self.ajouter_machine,
            on_actualiser=self.actualiser_machines,
        )

        self.actualiser_machines()  # <-- première génération de la liste
        # 2. self.view existe déjà : le thread peut l'utiliser en sécurité
        self._start_ping_thread()

        # 3. Fermeture propre de la connexion SQLite quand on ferme la fenêtre
        self.view.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # 4. On lance réellement l'affichage (bloque ici jusqu'à fermeture)
        self.view.run()

    # ------------------------------------------------------------------
    # PARTIE PING (lit les machines depuis la BDD)
    # ------------------------------------------------------------------

    def actualiser_machines(self):
        """Relit la BDD et redessine la sidebar (thread principal uniquement)."""
        machines = self.db.get_machines()  # [(id, nom, ip), ...]
        liste = [(nom, self.derniers_statuts.get(ip)) for id_m, nom, ip in machines]
        self.view.actualiser_machines(liste)

    def ajouter_machine(self, ip, nom):
        """Appelée depuis la vue (thread principal) quand on clique sur 'Ajouter'."""
        succes = self.db.add_machine(nom, ip)
        heure = time.strftime("%H:%M:%S")
        if succes:
            self.view.ajouter_evenement(heure, nom, "Machine ajoutée")
            self.actualiser_machines()
        else:
            self.view.ajouter_evenement(heure, nom, "Erreur : IP déjà existante")

    def _boucle_ping(self):
        """Boucle infinie : ping toutes les machines de la BDD, toutes les X secondes."""
        while True:
            machines = self.db.get_machines()  # [(id, nom, ip), ...]

            for id_m, nom, ip in machines:
                en_ligne = ping(ip)
                statut = "En ligne" if en_ligne else "Hors ligne"
                heure = time.strftime("%H:%M:%S")

                statut_precedent = self.derniers_statuts.get(ip)  # None si jamais vu
                changement = statut_precedent is None or statut_precedent != en_ligne

                self.derniers_statuts[ip] = (
                    en_ligne  # on met à jour la mémoire dans tous les cas
                )

                if changement:
                    # On ne journalise en BDD et dans l'UI QUE si le statut a changé
                    self.db.add_evenement(ip, nom, statut)
                    self.view.root.after(0, self._mettre_a_jour_vue, heure, nom, statut)

            # Calcul des statistiques après un cycle complet de ping
            _, pannes = self.db.get_stats_globales()  # on garde juste le compteur de pannes
            machines_en_ligne = sum(1 for v in self.derniers_statuts.values() if v)
            total_machines = len(machines)
            dernier_scan = time.time()

            # Disponibilité = état RÉEL et ACTUEL du réseau (cohérent avec le graphique)
            disponibilite = (machines_en_ligne / total_machines * 100) if total_machines > 0 else 0

            self.view.root.after(
                0,
                self.view.mettre_a_jour_indicateurs,
                disponibilite,
                machines_en_ligne,
                total_machines,
                pannes,
                dernier_scan,
            )

            # Nouveau point pour le graphique d'évolution (% de machines en ligne à cet instant)
            self.historique_dispo.append(disponibilite)
            self.historique_dispo = self.historique_dispo[-60:]  # garde les 60 derniers cycles

            self.view.root.after(0, self.view.mettre_a_jour_graphique, self.historique_dispo)

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
