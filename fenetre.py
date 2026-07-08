import tkinter as tk
from tkinter import ttk, font

class PingMonitorDarkApp:
    """
    Ping Monitor — Tableau de bord (Mode Sombre)
    Interface de bureau moderne pour la surveillance des machines
    Adaptée en thème sombre à partir de la maquette HTML/CSS
    """

    # Palette de couleurs (Dark Theme)
    COLORS = {
        "surface_1": "#1A1A18",  # Fond principal (gris anthracite)
        "surface_2": "#242422",  # Cartes et en-tête (élévation)
        "border": "#33322F",  # Bordures fines
        "text_primary": "#F1EFE8",  # Blanc cassé
        "text_secondary": "#B4B2A9",  # Gris clair
        "text_muted": "#706F6A",  # Gris moyen
        "text_success": "#1D9E75",  # Vert succès
        "text_danger": "#E24B4A",  # Rouge danger
        "accent": "#3A86C8",  # Bleu accentué
        "body_bg": "#0F0F0E",  # Fond de l'application
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ping Monitor")
        self.root.geometry("1000x620")
        self.root.configure(bg=self.COLORS["body_bg"])
        self.root.resizable(True, True)

        # Polices
        self.font_small = font.Font(family="Segoe UI", size=9)
        self.font_medium = font.Font(family="Segoe UI", size=10)
        self.font_large = font.Font(family="Segoe UI", size=12, weight="bold")

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
        header = tk.Frame(main_frame, bg=self.COLORS["surface_2"], height=46)
        header.pack(fill=tk.X, side=tk.TOP, pady=(0, 0))
        header.pack_propagate(False)

        # Titre avec icône
        title_label = tk.Label(
            header,
            text="❤️ Ping Monitor — Tableau de bord",
            font=self.font_medium,
            fg=self.COLORS["text_primary"],
            bg=self.COLORS["surface_2"],
        )
        title_label.pack(side=tk.LEFT, padx=14, pady=10)

        # Séparateur
        separator = tk.Frame(main_frame, bg=self.COLORS["border"], height=1)
        separator.pack(fill=tk.X, side=tk.TOP)

        # ------ CORPS (2 colonnes) ------
        body = tk.Frame(main_frame, bg=self.COLORS["surface_1"])
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar gauche
        self.sidebar = tk.Frame(
            body, bg=self.COLORS["surface_1"], width=220, relief="flat"
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
            insertbackground=self.COLORS["text_primary"],  # Curseur clair
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

        # Liste des machines (simulée)
        machines_data = [
            ("Serveur Web", self.COLORS["text_success"]),
            ("Routeur", self.COLORS["text_success"]),
            ("Imprimante", self.COLORS["text_danger"]),
            ("PC Bureau 2", self.COLORS["text_success"]),
        ]

        for i, (name, color) in enumerate(machines_data):
            # Rond de couleur (Canvas)
            dot_canvas = tk.Canvas(
                machines_frame,
                width=10,
                height=10,
                bg=self.COLORS["surface_1"],
                highlightthickness=0,
            )
            dot_canvas.create_oval(0, 0, 10, 10, fill=color, outline="")
            dot_canvas.pack(side=tk.LEFT, pady=(2, 2))

            label_machine = tk.Label(
                machines_frame,
                text=name,
                font=self.font_small,
                fg=self.COLORS["text_primary"],
                bg=self.COLORS["surface_1"],
            )
            label_machine.pack(anchor=tk.W, pady=(2, 2), padx=(4, 0))

            if i < len(machines_data) - 1:
                sep_machine = tk.Frame(
                    machines_frame, bg=self.COLORS["border"], height=1
                )
                sep_machine.pack(fill=tk.X, pady=2)

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
        """Construit la zone de contenu principale en mode sombre."""
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
                font=self.font_large,
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

        # Canvas pour le graphique (fond sombre)
        canvas = tk.Canvas(
            inner_chart,
            height=70,
            bg=self.COLORS["surface_2"],
            highlightthickness=0,
        )
        canvas.pack(fill=tk.X, pady=(0, 0))

        # Données du graphique (identique au SVG)
        points = [
            (0, 40),
            (40, 40),
            (80, 20),
            (120, 20),
            (160, 20),
            (200, 60),
            (240, 60),
            (280, 20),
            (320, 20),
            (360, 20),
            (400, 20),
            (440, 20),
            (480, 45),
            (520, 20),
            (560, 20),
            (600, 20),
        ]
        canvas_width = canvas.winfo_width() if canvas.winfo_width() > 100 else 600
        scale_x = canvas_width / 600 if canvas_width > 0 else 1

        coords = []
        for x, y in points:
            coords.append(x * scale_x)
            coords.append(y)

        # Ligne verte (succès)
        canvas.create_line(
            coords,
            fill=self.COLORS["text_success"],
            width=2,
            smooth=False,
        )
        canvas.update_idletasks()

        # ----- LIGNE 3 : Journal des événements (tableau) -----
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
        label_log.pack(anchor=tk.W, pady=(0, 6))

        # Tableau avec ttk.Treeview (stylisé dark)
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Dark.Treeview",
            background=self.COLORS["surface_2"],
            foreground=self.COLORS["text_primary"],
            fieldbackground=self.COLORS["surface_2"],
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=self.COLORS["surface_2"],
            foreground=self.COLORS["text_muted"],
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 9),
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", "#33322F")],
        )

        tree = ttk.Treeview(
            inner_log,
            columns=("Heure", "Machine", "Evenement"),
            show="headings",
            height=3,
            style="Dark.Treeview",
        )

        tree.heading("Heure", text="Heure")
        tree.heading("Machine", text="Machine")
        tree.heading("Evenement", text="Événement")

        tree.column("Heure", width=120, anchor="w")
        tree.column("Machine", width=120, anchor="w")
        tree.column("Evenement", width=200, anchor="w")

        # Données avec couleurs conditionnelles
        events = [
            ("14:32:10", "Imprimante", "Hors ligne"),
            ("13:58:44", "Serveur Web", "En ligne"),
            ("13:20:02", "Serveur Web", "Hors ligne"),
        ]

        for event in events:
            color = self.COLORS["text_danger"] if "Hors ligne" in event[2] else self.COLORS["text_success"]
            tree.insert("", tk.END, values=event, tags=(color,))

        tree.tag_configure(self.COLORS["text_danger"], foreground=self.COLORS["text_danger"])
        tree.tag_configure(self.COLORS["text_success"], foreground=self.COLORS["text_success"])

        tree.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        # Séparateur en bas du tableau
        sep_log = tk.Frame(inner_log, bg=self.COLORS["border"], height=1)
        sep_log.pack(fill=tk.X, pady=(6, 0))


if __name__ == "__main__":
    app = PingMonitorDarkApp()