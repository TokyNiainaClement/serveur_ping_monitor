import tkinter as tk
from tkinter import ttk, font
import time


class PingMonitorDarkApp:
    """
    Ping Monitor — Tableau de bord (Mode Sombre)
    Interface de bureau moderne avec tableau parfaitement aligné
    et lignes de séparation horizontales
    """

    # Palette de couleurs (Dark Theme)
    COLORS = {
        "body_bg": "#0F0F0E",  # Fond de l'application
        "surface_1": "#1A1A18",  # Conteneur principal
        "surface_2": "#242422",  # Cartes, en-tête, tableau
        "border": "#33322F",  # Bordures et séparateurs
        "text_primary": "#F1EFE8",  # Texte principal
        "text_secondary": "#B4B2A9",  # Texte secondaire
        "text_muted": "#706F6A",  # Texte atténué
        "text_success": "#1D9E75",  # Succès / En ligne
        "text_danger": "#E24B4A",  # Danger / Hors ligne
    }

    def __init__(self, on_ajouter=None, on_actualiser=None):
        self.root = tk.Tk()
        self.on_ajouter = on_ajouter
        self.on_actualiser = on_actualiser
        self.root.title("Ping Monitor")
        self.root.geometry("1100x680")
        self.root.configure(bg=self.COLORS["body_bg"])
        self.root.resizable(True, True)

        # Polices
        self.font_small = ("Segoe UI", 9)
        self.font_medium = ("Segoe UI", 10)
        self.font_large = ("Segoe UI", 12, "bold")
        self.font_xlarge = ("Segoe UI", 20, "bold")

        self._build_ui()
        # ⚠️ mainloop() n'est PLUS appelé ici. Voir la méthode run().

    def run(self):
        """
        Démarre réellement la boucle d'affichage Tkinter.
        Séparée de __init__ pour que le contrôleur puisse récupérer
        l'instance (self.view) AVANT que la fenêtre ne bloque le programme.
        """
        self._tick_dernier_scan()  # démarre le compteur en direct
        self.root.mainloop()

    def _build_ui(self):
        """Construit l'interface complète en mode sombre."""
        # Conteneur principal
        main_frame = tk.Frame(
            self.root,
            bg=self.COLORS["surface_1"],
            relief="flat",
            bd=0,
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ------ EN-TÊTE ------
        header = tk.Frame(main_frame, bg=self.COLORS["surface_2"], height=48)
        header.pack(fill=tk.X, side=tk.TOP, pady=(0, 0))
        header.pack_propagate(False)

        title_label = tk.Label(
            header,
            text=" Ping Monitor — Tableau de bord",
            font=self.font_medium,
            fg=self.COLORS["text_primary"],
            bg=self.COLORS["surface_2"],
        )
        title_label.pack(side=tk.LEFT, padx=16, pady=10)

        # Bouton quitter l'application
        btn_quit = tk.Button(
            header,
            text="Quitter",
            font=self.font_small,
            bg=self.COLORS["surface_2"],
            fg=self.COLORS["text_primary"],
            relief="flat",
            bd=1,
            highlightthickness=0,
            cursor="hand2",
            activebackground=self.COLORS["border"],
            activeforeground=self.COLORS["text_primary"],
            command=self.root.quit
        )
        btn_quit.pack(side=tk.LEFT, padx=16, pady=10)

        # Bouton gérer
        btn_manage = tk.Button(
            header,
            text="Gérer",
            font=self.font_small,
            bg=self.COLORS["surface_2"],
            fg=self.COLORS["text_primary"],
            relief="flat",
            bd=1,
            highlightthickness=0,
            cursor="hand2",
            activebackground=self.COLORS["border"],
            activeforeground=self.COLORS["text_primary"]
        )
        btn_manage.pack(side=tk.LEFT, padx=16, pady=10)

        # Séparateur
        separator = tk.Frame(main_frame, bg=self.COLORS["border"], height=1)
        separator.pack(fill=tk.X, side=tk.TOP)

        # ------ CORPS (2 colonnes) ------
        body = tk.Frame(main_frame, bg=self.COLORS["surface_1"])
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar gauche
        self.sidebar = tk.Frame(
            body, bg=self.COLORS["surface_1"], width=230, relief="flat"
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 0), pady=(0, 0))
        self.sidebar.pack_propagate(False)

        # Contenu principal
        self.content = tk.Frame(body, bg=self.COLORS["surface_1"])
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_sidebar()
        self._build_content()

    def _build_sidebar(self):
        """Construit la sidebar gauche en mode sombre."""
        pad = tk.Frame(self.sidebar, bg=self.COLORS["surface_1"], height=10)
        pad.pack()

        # Section "Ajouter une machine"
        add_frame = tk.Frame(self.sidebar, bg=self.COLORS["surface_1"])
        add_frame.pack(fill=tk.X, padx=14, pady=(0, 12))

        label_add = tk.Label(
            add_frame,
            text="Ajouter une machine",
            font=self.font_small,
            fg=self.COLORS["text_muted"],
            bg=self.COLORS["surface_1"],
        )
        label_add.pack(anchor=tk.W)

        # Champ IP
        self.placeholder_ip = "192.168.1.10"
        self.entry_ip = tk.Entry(
            add_frame,
            font=self.font_small,
            bg=self.COLORS["surface_2"],
            fg=self.COLORS["text_muted"],
            relief="flat",
            bd=1,
            highlightthickness=0,
            insertbackground=self.COLORS["text_primary"],
        )
        self.entry_ip.pack(fill=tk.X, pady=(4, 4))
        self.entry_ip.insert(0, self.placeholder_ip)
        self.entry_ip.bind(
            "<FocusIn>",
            lambda e: self._effacer_placeholder(self.entry_ip, self.placeholder_ip),
        )
        self.entry_ip.bind(
            "<FocusOut>",
            lambda e: self._restaurer_placeholder(self.entry_ip, self.placeholder_ip),
        )
        self.entry_ip.config(fg=self.COLORS["text_secondary"])

        # Champ nom
        self.placeholder_nom = "Nom (optionnel)"
        self.entry_name = tk.Entry(
            add_frame,
            font=self.font_small,
            bg=self.COLORS["surface_2"],
            fg=self.COLORS["text_muted"],
            relief="flat",
            bd=1,
            highlightthickness=0,
            insertbackground=self.COLORS["text_primary"],
        )
        self.entry_name.pack(fill=tk.X, pady=(0, 6))
        self.entry_name.insert(0, self.placeholder_nom)
        self.entry_name.bind(
            "<FocusIn>",
            lambda e: self._effacer_placeholder(self.entry_name, self.placeholder_nom),
        )
        self.entry_name.bind(
            "<FocusOut>",
            lambda e: self._restaurer_placeholder(
                self.entry_name, self.placeholder_nom
            ),
        )
        # self.entry_name.insert(0, "Nom (optionnel)")

        # Bouton Ajouter
        btn_add = tk.Button(
            add_frame,
            text="➕ Ajouter",
            font=self.font_small,
            bg=self.COLORS["surface_2"],
            fg=self.COLORS["text_primary"],
            relief="flat",
            bd=1,
            highlightthickness=0,
            cursor="hand2",
            activebackground=self.COLORS["border"],
            activeforeground=self.COLORS["text_primary"],
            command=self._on_clic_ajouter,  # <-- ligne ajoutée
        )
        btn_add.pack(fill=tk.X, pady=(0, 0))

        # Séparateur
        sep = tk.Frame(self.sidebar, bg=self.COLORS["border"], height=1)
        sep.pack(fill=tk.X, padx=14, pady=8)

        # Section "Machines surveillées"
        # Section "Machines surveillées"
        machines_frame = tk.Frame(self.sidebar, bg=self.COLORS["surface_1"])
        machines_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 0))

        header_machines = tk.Frame(machines_frame, bg=self.COLORS["surface_1"])
        header_machines.pack(fill=tk.X, pady=(0, 6))

        label_machines = tk.Label(
            header_machines,
            text="Machines surveillées",
            font=self.font_small,
            fg=self.COLORS["text_muted"],
            bg=self.COLORS["surface_1"],
        )
        label_machines.pack(side=tk.LEFT, anchor=tk.W)

        btn_refresh = tk.Button(
            header_machines,
            text="🔄",
            font=self.font_small,
            bg=self.COLORS["surface_1"],
            fg=self.COLORS["text_muted"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            activeforeground=self.COLORS["text_primary"],
            command=self._on_clic_actualiser,
        )
        btn_refresh.pack(side=tk.RIGHT)

        # Zone scrollable pour la liste des machines
        self.machines_canvas = tk.Canvas(
            machines_frame,
            bg=self.COLORS["surface_1"],
            highlightthickness=0,
        )
        machines_scrollbar = tk.Scrollbar(
            machines_frame,
            orient="vertical",
            command=self.machines_canvas.yview,
        )
        self.machines_canvas.configure(yscrollcommand=machines_scrollbar.set)

        self.machines_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        machines_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Conteneur redessiné à chaque actualisation (placé DANS le canvas)
        self.liste_machines_container = tk.Frame(
            self.machines_canvas, bg=self.COLORS["surface_1"]
        )
        self.machines_canvas_window = self.machines_canvas.create_window(
            (0, 0), window=self.liste_machines_container, anchor="nw"
        )

        self.liste_machines_container.bind(
            "<Configure>",
            lambda e: self.machines_canvas.configure(scrollregion=self.machines_canvas.bbox("all")),
        )
        self.machines_canvas.bind(
            "<Configure>",
            lambda e: self.machines_canvas.itemconfig(self.machines_canvas_window, width=e.width),
        )

        # Molette de souris active SEULEMENT quand le curseur survole la sidebar
        # (évite un conflit avec le scroll du tableau des événements)
        def _on_mousewheel_sidebar(event):
            if event.num == 5 or event.delta < 0:
                self.machines_canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                self.machines_canvas.yview_scroll(-1, "units")

        def _bind_scroll_sidebar(event):
            self.machines_canvas.bind_all("<MouseWheel>", _on_mousewheel_sidebar)
            self.machines_canvas.bind_all("<Button-4>", _on_mousewheel_sidebar)
            self.machines_canvas.bind_all("<Button-5>", _on_mousewheel_sidebar)

        def _unbind_scroll_sidebar(event):
            self.machines_canvas.unbind_all("<MouseWheel>")
            self.machines_canvas.unbind_all("<Button-4>")
            self.machines_canvas.unbind_all("<Button-5>")

        self.machines_canvas.bind("<Enter>", _bind_scroll_sidebar)
        self.machines_canvas.bind("<Leave>", _unbind_scroll_sidebar)

        self._dessiner_machines([])  # vide au démarrage

        # Section "Intervalle" (en bas)
        interval_frame = tk.Frame(self.sidebar, bg=self.COLORS["surface_1"])
        interval_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=14, pady=(0, 10))

        sep_bottom = tk.Frame(interval_frame, bg=self.COLORS["border"], height=1)
        sep_bottom.pack(fill=tk.X, pady=(0, 6))

        interval_label = tk.Label(
            interval_frame,
            text="⏱️ Intervalle : 10s",
            font=self.font_small,
            fg=self.COLORS["text_muted"],
            bg=self.COLORS["surface_1"],
        )
        interval_label.pack(anchor=tk.W)

    def _build_content(self):
        """Construit la zone de contenu principale avec tableau parfaitement aligné."""
        content_pad = tk.Frame(self.content, bg=self.COLORS["surface_1"])
        content_pad.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        # ----- LIGNE 1 : 4 indicateurs -----
        indicators_frame = tk.Frame(content_pad, bg=self.COLORS["surface_1"])
        indicators_frame.pack(fill=tk.X, pady=(0, 14))

        indicators = [
            ("Disponibilité globale", "—", self.COLORS["text_primary"]),
            ("Machines en ligne", "0 / 0", self.COLORS["text_success"]),
            ("Pannes détectées", "0", self.COLORS["text_primary"]),
            ("Dernier scan", "—", self.COLORS["text_primary"]),
        ]

        self.indicator_labels = {}   # <-- ligne ajoutée : pour retrouver chaque label ensuite

        for i, (title, value, color) in enumerate(indicators):
            card = tk.Frame(
                indicators_frame,
                bg=self.COLORS["surface_2"],
                relief="flat",
                bd=0,
            )
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            if i == 3:
                card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 0))

            inner = tk.Frame(card, bg=self.COLORS["surface_2"])
            inner.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

            label_title = tk.Label(
                inner,
                text=title,
                font=self.font_small,
                fg=self.COLORS["text_secondary"],
                bg=self.COLORS["surface_2"],
            )
            label_title.pack(anchor=tk.W)

            label_value = tk.Label(
                inner,
                text=value,
                font=self.font_xlarge,
                fg=color,
                bg=self.COLORS["surface_2"],
            )
            label_value.pack(anchor=tk.W)
            self.indicator_labels[title] = label_value   # <-- garde une référence pour mise à jour

        # ----- LIGNE 2 : Graphique -----
        chart_frame = tk.Frame(
            content_pad, bg=self.COLORS["surface_2"], relief="flat", bd=0
        )
        chart_frame.pack(fill=tk.X, pady=(0, 14))

        inner_chart = tk.Frame(chart_frame, bg=self.COLORS["surface_2"])
        inner_chart.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        label_chart = tk.Label(
            inner_chart,
            text="Évolution récente",
            font=self.font_medium,
            fg=self.COLORS["text_primary"],
            bg=self.COLORS["surface_2"],
        )
        label_chart.pack(anchor=tk.W, pady=(0, 6))

        # Canvas pour le graphique (stocké en attribut pour être redessiné plus tard)
        self.chart_canvas = tk.Canvas(
            inner_chart,
            height=90,
            bg=self.COLORS["surface_2"],
            highlightthickness=0,
        )
        self.chart_canvas.pack(fill=tk.X, pady=(0, 0))

        # Historique des valeurs de disponibilité (%) affichées sur le graphique
        self.historique_dispo = []

        # ----- LIGNE 3 : Journal des événements (tableau dynamique) -----
        log_frame = tk.Frame(
            content_pad, bg=self.COLORS["surface_2"], relief="flat", bd=0
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        inner_log = tk.Frame(log_frame, bg=self.COLORS["surface_2"])
        inner_log.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        label_log = tk.Label(
            inner_log,
            text="Journal des événements",
            font=self.font_medium,
            fg=self.COLORS["text_primary"],
            bg=self.COLORS["surface_2"],
        )
        label_log.pack(anchor=tk.W, pady=(0, 8))

        # ----- ZONE SCROLLABLE (Canvas + Scrollbar) -----
        # Tkinter n'a pas de "zone scrollable" native : on simule ça avec
        # un Canvas (qui peut défiler) contenant un Frame (le vrai tableau).
        scroll_frame = tk.Frame(inner_log, bg=self.COLORS["surface_2"])
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.log_canvas = tk.Canvas(
            scroll_frame,
            bg=self.COLORS["surface_2"],
            highlightthickness=0,
        )
        scrollbar = tk.Scrollbar(
            scroll_frame,
            orient="vertical",
            command=self.log_canvas.yview,
        )
        self.log_canvas.configure(yscrollcommand=scrollbar.set)

        self.log_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ----- TABLEAU AVEC GRID ET SÉPARATEURS (placé DANS le canvas) -----
        table_container = tk.Frame(self.log_canvas, bg=self.COLORS["surface_2"])
        self.log_canvas_window = self.log_canvas.create_window(
            (0, 0), window=table_container, anchor="nw"
        )

        # Configuration de la grille avec des poids égaux
        table_container.grid_columnconfigure(0, weight=1, uniform="col")
        table_container.grid_columnconfigure(1, weight=1, uniform="col")
        table_container.grid_columnconfigure(2, weight=1, uniform="col")

        # Quand le contenu du tableau change de taille, on met à jour
        # la zone défilable du canvas en conséquence.
        table_container.bind(
            "<Configure>",
            lambda e: self.log_canvas.configure(
                scrollregion=self.log_canvas.bbox("all")
            ),
        )
        # Quand le canvas change de largeur (redimensionnement fenêtre),
        # le tableau à l'intérieur doit s'étirer pareil.
        self.log_canvas.bind(
            "<Configure>",
            lambda e: self.log_canvas.itemconfig(self.log_canvas_window, width=e.width),
        )

        # Molette de la souris → défilement (Linux : Button-4/5, Windows/Mac : MouseWheel)
        def _on_mousewheel(event):
            if event.num == 5 or event.delta < 0:
                self.log_canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                self.log_canvas.yview_scroll(-1, "units")

        self.log_canvas.bind_all("<Button-4>", _on_mousewheel)
        self.log_canvas.bind_all("<Button-5>", _on_mousewheel)
        self.log_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ----- EN-TÊTES -----
        headers = ["Heure", "Machine", "Événement"]
        for col, header in enumerate(headers):
            label = tk.Label(
                table_container,
                text=header,
                font=self.font_small,
                fg=self.COLORS["text_muted"],
                bg=self.COLORS["surface_2"],
                anchor="w",
            )
            label.grid(row=0, column=col, sticky="w", padx=(2, 0), pady=(0, 4))

        # Séparateur sous l'en-tête
        sep_header = tk.Frame(
            table_container,
            bg=self.COLORS["border"],
            height=1,
        )
        sep_header.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 6))

        # Le tableau démarre vide : les lignes seront ajoutées dynamiquement
        # par ajouter_evenement(), appelée depuis le contrôleur.
        self.table_container = table_container
        self._log_next_row = 2  # prochaine ligne grid disponible

    # ------------------------------------------------------------------
    # MÉTHODE PUBLIQUE : appelée par le contrôleur pour ajouter une ligne
    # ------------------------------------------------------------------

    def _effacer_placeholder(self, entry, placeholder):
        """Vide le champ et repasse en couleur normale s'il contient encore le placeholder."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.COLORS["text_primary"])

    def _restaurer_placeholder(self, entry, placeholder):
        """Remet le placeholder si l'utilisateur a laissé le champ vide."""
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg=self.COLORS["text_muted"])

    def _dessiner_machines(self, machines):
        """machines : liste de tuples (nom, en_ligne) — en_ligne = True/False/None."""
        for widget in self.liste_machines_container.winfo_children():
            widget.destroy()

        for nom, en_ligne in machines:
            if en_ligne is True:
                color = self.COLORS["text_success"]
            elif en_ligne is False:
                color = self.COLORS["text_danger"]
            else:
                color = self.COLORS["text_muted"]

            line_frame = tk.Frame(
                self.liste_machines_container, bg=self.COLORS["surface_1"]
            )
            line_frame.pack(fill=tk.X, pady=(1, 1))

            dot_canvas = tk.Canvas(
                line_frame,
                width=10,
                height=10,
                bg=self.COLORS["surface_1"],
                highlightthickness=0,
            )
            dot_canvas.create_oval(0, 0, 10, 10, fill=color, outline="")
            dot_canvas.pack(side=tk.LEFT, padx=(8, 4), pady=6)

            label_machine = tk.Label(
                line_frame,
                text=nom,
                font=self.font_small,
                fg=self.COLORS["text_primary"],
                bg=self.COLORS["surface_1"],
            )
            label_machine.pack(anchor=tk.W, pady=6, padx=(0, 8))

    def actualiser_machines(self, machines):
        """Méthode publique appelée par le contrôleur pour rafraîchir la sidebar."""
        self._dessiner_machines(machines)

    def _on_clic_actualiser(self):
        if self.on_actualiser:
            self.on_actualiser()

    def _on_clic_ajouter(self):
        """Lit les champs IP/Nom et transmet au contrôleur via le callback."""
        ip = self.entry_ip.get().strip()
        nom = self.entry_name.get().strip()

        # Ignore le texte de placeholder si l'utilisateur n'a rien tapé
        if ip == "192.168.1.10" or ip == "":
            return
        if nom == "Nom (optionnel)" or nom == "":
            nom = ip  # nom par défaut = IP

        if self.on_ajouter:
            self.on_ajouter(ip, nom)

        # Réinitialise les champs après l'ajout
        self.entry_ip.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, "Nom (optionnel)")

    
    def mettre_a_jour_indicateurs(self, disponibilite, machines_en_ligne, total_machines, pannes, dernier_scan_ts):
        """Appelée par le contrôleur (thread principal) pour rafraîchir les 4 cartes du haut."""
        self.indicator_labels["Disponibilité globale"].config(text=f"{disponibilite:.0f}%")
        self.indicator_labels["Machines en ligne"].config(text=f"{machines_en_ligne} / {total_machines}")
        self.indicator_labels["Pannes détectées"].config(text=str(pannes))
        self.dernier_scan_ts = dernier_scan_ts  # timestamp, affiché en direct par _tick_dernier_scan

    def _tick_dernier_scan(self):
        """Rafraîchit le libellé 'Dernier scan' chaque seconde (compteur en direct)."""
        if hasattr(self, "dernier_scan_ts"):
            secondes = int(time.time() - self.dernier_scan_ts)
            self.indicator_labels["Dernier scan"].config(text=f"il y a {secondes}s")
        self.root.after(1000, self._tick_dernier_scan)  # se replanifie lui-même
        
    def mettre_a_jour_graphique(self, valeurs):
        """
        Redessine le graphique d'évolution à partir d'une liste de %
        de disponibilité, avec grille de repère et valeur actuelle affichée.
        """
        self.chart_canvas.delete("all")

        largeur = self.chart_canvas.winfo_width() or 600
        hauteur = 90
        marge_gauche = 34   # espace réservé pour les labels "0% / 50% / 100%"
        marge_haut = 8
        marge_bas = 8
        zone_haut = hauteur - marge_haut - marge_bas

        # ----- Grille horizontale + labels de pourcentage -----
        for pct in (0, 50, 100):
            y = marge_haut + zone_haut - (pct / 100) * zone_haut
            self.chart_canvas.create_line(
                marge_gauche, y, largeur, y,
                fill=self.COLORS["border"], width=1, dash=(2, 3),
            )
            self.chart_canvas.create_text(
                marge_gauche - 6, y,
                text=f"{pct}%",
                fill=self.COLORS["text_muted"],
                font=self.font_small,
                anchor="e",
            )

        if len(valeurs) < 2:
            self.chart_canvas.create_text(
                (largeur + marge_gauche) / 2, hauteur / 2,
                text="En attente de données...",
                fill=self.COLORS["text_muted"],
                font=self.font_small,
            )
            return

        # ----- Tracé de la courbe -----
        pas_x = (largeur - marge_gauche - 10) / (len(valeurs) - 1)
        coords = []
        for i, valeur in enumerate(valeurs):
            x = marge_gauche + i * pas_x
            y = marge_haut + zone_haut - (valeur / 100) * zone_haut
            coords.extend([x, y])

        derniere_valeur = valeurs[-1]
        couleur = self.COLORS["text_success"] if derniere_valeur >= 50 else self.COLORS["text_danger"]

        self.chart_canvas.create_line(coords, fill=couleur, width=2, smooth=True)

        # Point + étiquette sur la dernière valeur (valeur actuelle)
        dernier_x, dernier_y = coords[-2], coords[-1]
        self.chart_canvas.create_oval(
            dernier_x - 3, dernier_y - 3, dernier_x + 3, dernier_y + 3,
            fill=couleur, outline="",
        )
        self.chart_canvas.create_text(
            dernier_x, dernier_y - 12,
            text=f"{derniere_valeur:.0f}%",
            fill=couleur,
            font=self.font_small,
            anchor="s",
        )

    def ajouter_evenement(self, heure, machine, evenement):
        """
        Ajoute une ligne au journal des événements.

        ⚠️ Cette méthode manipule des widgets Tkinter : elle doit TOUJOURS
        être appelée depuis le thread principal (via root.after(0, ...)),
        jamais directement depuis le thread de ping.
        """
        row = self._log_next_row

        # Séparateur avant la nouvelle ligne (sauf la toute première)
        if row > 2:
            sep_line = tk.Frame(
                self.table_container, bg=self.COLORS["border"], height=1
            )
            sep_line.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(4, 4))
            row += 1

        event_color = (
            self.COLORS["text_danger"]
            if "Hors ligne" in evenement
            else self.COLORS["text_success"]
        )
        valeurs = (heure, machine, evenement)
        couleurs = (
            self.COLORS["text_secondary"],
            self.COLORS["text_primary"],
            event_color,
        )

        for col, (valeur, couleur) in enumerate(zip(valeurs, couleurs)):
            label = tk.Label(
                self.table_container,
                text=valeur,
                font=self.font_small,
                fg=couleur,
                bg=self.COLORS["surface_2"],
                anchor="w",
            )
            label.grid(row=row, column=col, sticky="w", padx=(2, 0), pady=(2, 2))

        self._log_next_row = row + 1

        # Défilement automatique vers le bas pour voir le dernier événement
        self.log_canvas.update_idletasks()
        self.log_canvas.configure(scrollregion=self.log_canvas.bbox("all"))
        self.log_canvas.yview_moveto(1.0)


if __name__ == "__main__":
    app = PingMonitorDarkApp()
    app.run()
