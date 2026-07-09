import tkinter as tk
from tkinter import ttk, font

class PingMonitorDarkApp:
    """
    Ping Monitor — Tableau de bord (Mode Sombre)
    Interface de bureau moderne avec tableau parfaitement aligné
    et lignes de séparation horizontales
    """

    # Palette de couleurs (Dark Theme)
    COLORS = {
        "body_bg": "#0F0F0E",           # Fond de l'application
        "surface_1": "#1A1A18",          # Conteneur principal
        "surface_2": "#242422",          # Cartes, en-tête, tableau
        "border": "#33322F",             # Bordures et séparateurs
        "text_primary": "#F1EFE8",       # Texte principal
        "text_secondary": "#B4B2A9",     # Texte secondaire
        "text_muted": "#706F6A",         # Texte atténué
        "text_success": "#1D9E75",       # Succès / En ligne
        "text_danger": "#E24B4A",        # Danger / Hors ligne
    }

    def __init__(self):
        self.root = tk.Tk()
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
        self.entry_ip = tk.Entry(
            add_frame,
            font=self.font_small,
            bg=self.COLORS["surface_2"],
            fg=self.COLORS["text_primary"],
            relief="flat",
            bd=1,
            highlightthickness=0,
            insertbackground=self.COLORS["text_primary"],
        )
        self.entry_ip.pack(fill=tk.X, pady=(4, 4))
        self.entry_ip.insert(0, "192.168.1.10")
        self.entry_ip.config(fg=self.COLORS["text_secondary"])

        # Champ nom
        self.entry_name = tk.Entry(
            add_frame,
            font=self.font_small,
            bg=self.COLORS["surface_2"],
            fg=self.COLORS["text_secondary"],
            relief="flat",
            bd=1,
            highlightthickness=0,
            insertbackground=self.COLORS["text_primary"],
        )
        self.entry_name.pack(fill=tk.X, pady=(0, 6))
        self.entry_name.insert(0, "Nom (optionnel)")

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
        )
        btn_add.pack(fill=tk.X, pady=(0, 0))

        # Séparateur
        sep = tk.Frame(self.sidebar, bg=self.COLORS["border"], height=1)
        sep.pack(fill=tk.X, padx=14, pady=8)

        # Section "Machines surveillées"
        machines_frame = tk.Frame(self.sidebar, bg=self.COLORS["surface_1"])
        machines_frame.pack(fill=tk.X, padx=14, pady=(0, 0))

        label_machines = tk.Label(
            machines_frame,
            text="Machines surveillées",
            font=self.font_small,
            fg=self.COLORS["text_muted"],
            bg=self.COLORS["surface_1"],
        )
        label_machines.pack(anchor=tk.W, pady=(0, 6))

        # Liste des machines
        machines_data = [
            ("Serveur Web", self.COLORS["text_success"], True),
            ("Routeur", self.COLORS["text_success"], False),
            ("Imprimante", self.COLORS["text_danger"], False),
            ("PC Bureau 2", self.COLORS["text_success"], False),
        ]

        for i, (name, color, selected) in enumerate(machines_data):
            # Conteneur de ligne
            line_bg = self.COLORS["surface_2"] if selected else self.COLORS["surface_1"]
            line_frame = tk.Frame(
                machines_frame,
                bg=line_bg,
                relief="flat",
                bd=0,
            )
            line_frame.pack(fill=tk.X, pady=(1, 1))

            # Puce colorée (Canvas pour un cercle parfait)
            dot_canvas = tk.Canvas(
                line_frame,
                width=10,
                height=10,
                bg=line_bg,
                highlightthickness=0,
            )
            dot_canvas.create_oval(0, 0, 10, 10, fill=color, outline="")
            dot_canvas.pack(side=tk.LEFT, padx=(8, 4), pady=6)

            # Nom de la machine
            label_machine = tk.Label(
                line_frame,
                text=name,
                font=self.font_small,
                fg=self.COLORS["text_primary"],
                bg=line_bg,
            )
            label_machine.pack(anchor=tk.W, pady=6, padx=(0, 8))

        # Espace pour pousser l'intervalle en bas
        spacer = tk.Frame(self.sidebar, bg=self.COLORS["surface_1"], height=10)
        spacer.pack(fill=tk.BOTH, expand=True)

        # Section "Intervalle" (en bas)
        interval_frame = tk.Frame(
            self.sidebar, bg=self.COLORS["surface_1"]
        )
        interval_frame.pack(
            fill=tk.X, side=tk.BOTTOM, padx=14, pady=(0, 10)
        )

        sep_bottom = tk.Frame(
            interval_frame, bg=self.COLORS["border"], height=1
        )
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
        content_pad = tk.Frame(
            self.content, bg=self.COLORS["surface_1"]
        )
        content_pad.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        # ----- LIGNE 1 : 4 indicateurs -----
        indicators_frame = tk.Frame(content_pad, bg=self.COLORS["surface_1"])
        indicators_frame.pack(fill=tk.X, pady=(0, 14))

        indicators = [
            ("Disponibilité globale", "92%", self.COLORS["text_primary"]),
            ("Machines en ligne", "3 / 4", self.COLORS["text_success"]),
            ("Pannes détectées", "7", self.COLORS["text_primary"]),
            ("Dernier scan", "il y a 4s", self.COLORS["text_primary"]),
        ]

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

        # ----- LIGNE 2 : Graphique -----
        chart_frame = tk.Frame(
            content_pad, bg=self.COLORS["surface_2"], relief="flat", bd=0
        )
        chart_frame.pack(fill=tk.X, pady=(0, 14))

        inner_chart = tk.Frame(chart_frame, bg=self.COLORS["surface_2"])
        inner_chart.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        label_chart = tk.Label(
            inner_chart,
            text="Évolution de l'état (24h)",
            font=self.font_medium,
            fg=self.COLORS["text_primary"],
            bg=self.COLORS["surface_2"],
        )
        label_chart.pack(anchor=tk.W, pady=(0, 6))

        # Canvas pour le graphique
        canvas = tk.Canvas(
            inner_chart,
            height=70,
            bg=self.COLORS["surface_2"],
            highlightthickness=0,
        )
        canvas.pack(fill=tk.X, pady=(0, 0))

        # Données du graphique
        points = [
            (0, 40), (40, 40), (80, 20), (120, 20), (160, 20),
            (200, 60), (240, 60), (280, 20), (320, 20), (360, 20),
            (400, 20), (440, 20), (480, 45), (520, 20), (560, 20), (600, 20),
        ]
        
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width() if canvas.winfo_width() > 100 else 600
        scale_x = canvas_width / 600 if canvas_width > 0 else 1

        coords = []
        for x, y in points:
            coords.append(x * scale_x)
            coords.append(y)

        canvas.create_line(
            coords,
            fill=self.COLORS["text_success"],
            width=2,
            smooth=False,
        )

        # ----- LIGNE 3 : Journal des événements (Tableau avec Grid et séparateurs) -----
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

        # ----- TABLEAU AVEC GRID ET SÉPARATEURS -----
        table_container = tk.Frame(inner_log, bg=self.COLORS["surface_2"])
        table_container.pack(fill=tk.BOTH, expand=True)

        # Configuration de la grille avec des poids égaux
        table_container.grid_columnconfigure(0, weight=1, uniform="col")
        table_container.grid_columnconfigure(1, weight=1, uniform="col")
        table_container.grid_columnconfigure(2, weight=1, uniform="col")

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

        # ----- DONNÉES DU TABLEAU AVEC SÉPARATEURS -----
        events = [
            ("14:32:10", "Imprimante", "Hors ligne"),
            ("13:58:44", "Serveur Web", "En ligne"),
            ("13:20:02", "Serveur Web", "Hors ligne"),
        ]

        # On commence à la ligne 2 (row=2)
        current_row = 2
        
        for i, event in enumerate(events):
            # Déterminer la couleur de l'événement
            event_color = self.COLORS["text_danger"] if "Hors ligne" in event[2] else self.COLORS["text_success"]
            
            # Afficher les données
            for col, value in enumerate(event):
                # Déterminer la couleur pour chaque colonne
                if col == 0:  # Heure
                    color = self.COLORS["text_secondary"]
                elif col == 1:  # Machine
                    color = self.COLORS["text_primary"]
                else:  # Événement
                    color = event_color
                
                label = tk.Label(
                    table_container,
                    text=value,
                    font=self.font_small,
                    fg=color,
                    bg=self.COLORS["surface_2"],
                    anchor="w",
                )
                label.grid(row=current_row, column=col, sticky="w", padx=(2, 0), pady=(2, 2))

            # Ajouter une ligne de séparation horizontale SAUF après la dernière ligne
            if i < len(events) - 1:
                sep_line = tk.Frame(
                    table_container,
                    bg=self.COLORS["border"],
                    height=1,
                )
                sep_line.grid(row=current_row + 1, column=0, columnspan=3, sticky="ew", pady=(4, 4))
                current_row += 2
            else:
                current_row += 1


if __name__ == "__main__":
    app = PingMonitorDarkApp()