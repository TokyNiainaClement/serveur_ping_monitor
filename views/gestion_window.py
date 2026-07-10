import tkinter as tk
from tkinter import ttk, messagebox


class GestionWindow(tk.Toplevel):
    """
    Fenêtre secondaire : gestion des machines surveillées.
    - Tableau de toutes les machines (nom + IP)
    - Modification du nom / de l'IP d'une machine sélectionnée
    - Suppression d'une machine
    - Tableau d'historique des événements (global, ou filtré sur la machine sélectionnée)
    """

    # Même palette que la fenêtre principale, pour une interface cohérente
    COLORS = {
        "body_bg": "#0F0F0E",
        "surface_1": "#1A1A18",
        "surface_2": "#242422",
        "border": "#33322F",
        "text_primary": "#F1EFE8",
        "text_secondary": "#B4B2A9",
        "text_muted": "#706F6A",
        "text_success": "#1D9E75",
        "text_danger": "#E24B4A",
    }

    def __init__(self, master, get_machines, get_evenements, on_modifier, on_supprimer, on_effacer_historique):
        """
        get_machines()             -> [(id, nom, ip), ...]
        get_evenements(ip=None)    -> [(id, heure, ip, nom, evenement), ...]
        on_modifier(id, nom, ip)   -> bool (succès)
        on_supprimer(id)           -> None
        """
        super().__init__(master)
        self.get_machines = get_machines
        self.get_evenements = get_evenements
        self.on_modifier = on_modifier
        self.on_supprimer = on_supprimer
        self.on_effacer_historique = on_effacer_historique
        self.ip_filtre_historique = None  # None = historique global, sinon IP de la machine sélectionnée

        self.title("Gestion des machines")
        self.geometry("700x600")
        self.configure(bg=self.COLORS["body_bg"])

        self.font_small = ("Segoe UI", 9)
        self.font_medium = ("Segoe UI", 10)

        self.machine_selectionnee = None  # id de la machine actuellement sélectionnée

        self._configurer_style_treeview()
        self._build_ui()
        self._charger_machines()
        self._charger_historique()

    # ------------------------------------------------------------------
    # STYLE (Treeview ttk ne supporte pas bg/fg directement comme tk.Label)
    # ------------------------------------------------------------------

    def _configurer_style_treeview(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Dark.Treeview",
            background=self.COLORS["surface_2"],
            fieldbackground=self.COLORS["surface_2"],
            foreground=self.COLORS["text_primary"],
            rowheight=26,
            borderwidth=0,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=self.COLORS["surface_1"],
            foreground=self.COLORS["text_muted"],
            borderwidth=0,
            font=self.font_small,
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", self.COLORS["border"])],
            foreground=[("selected", self.COLORS["text_primary"])],
        )

    # ------------------------------------------------------------------
    # CONSTRUCTION DE L'INTERFACE
    # ------------------------------------------------------------------

    def _build_ui(self):
        main = tk.Frame(self, bg=self.COLORS["body_bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # ----- Section : liste des machines -----
        label_machines = tk.Label(
            main,
            text="Machines surveillées",
            font=self.font_medium,
            fg=self.COLORS["text_primary"],
            bg=self.COLORS["body_bg"],
        )
        label_machines.pack(anchor=tk.W, pady=(0, 6))

        self.tree_machines = ttk.Treeview(
            main,
            columns=("nom", "ip"),
            show="headings",
            style="Dark.Treeview",
            height=8,
            selectmode="browse",
        )
        self.tree_machines.heading("nom", text="Nom")
        self.tree_machines.heading("ip", text="Adresse IP")
        self.tree_machines.column("nom", width=250)
        self.tree_machines.column("ip", width=200)
        self.tree_machines.pack(fill=tk.X, pady=(0, 8))
        self.tree_machines.bind("<<TreeviewSelect>>", self._on_selection_machine)

        # ----- Section : formulaire d'édition -----
        form_frame = tk.Frame(main, bg=self.COLORS["surface_2"])
        form_frame.pack(fill=tk.X, pady=(0, 14))

        inner_form = tk.Frame(form_frame, bg=self.COLORS["surface_2"])
        inner_form.pack(fill=tk.X, padx=12, pady=10)

        tk.Label(
            inner_form,
            text="Nom :",
            font=self.font_small,
            fg=self.COLORS["text_muted"],
            bg=self.COLORS["surface_2"],
        ).grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)

        self.entry_nom = tk.Entry(
            inner_form,
            font=self.font_small,
            bg=self.COLORS["body_bg"],
            fg=self.COLORS["text_primary"],
            relief="flat",
            insertbackground=self.COLORS["text_primary"],
        )
        self.entry_nom.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=4)

        tk.Label(
            inner_form,
            text="IP :",
            font=self.font_small,
            fg=self.COLORS["text_muted"],
            bg=self.COLORS["surface_2"],
        ).grid(row=0, column=2, sticky="w", padx=(0, 6), pady=4)

        self.entry_ip = tk.Entry(
            inner_form,
            font=self.font_small,
            bg=self.COLORS["body_bg"],
            fg=self.COLORS["text_primary"],
            relief="flat",
            insertbackground=self.COLORS["text_primary"],
        )
        self.entry_ip.grid(row=0, column=3, sticky="ew", pady=4)

        inner_form.grid_columnconfigure(1, weight=1)
        inner_form.grid_columnconfigure(3, weight=1)

        btn_frame = tk.Frame(inner_form, bg=self.COLORS["surface_2"])
        btn_frame.grid(row=1, column=0, columnspan=4, sticky="w", pady=(10, 0))

        self.btn_enregistrer = tk.Button(
            btn_frame,
            text="💾 Enregistrer les modifications",
            font=self.font_small,
            bg=self.COLORS["surface_1"],
            fg=self.COLORS["text_primary"],
            relief="flat",
            bd=1,
            cursor="hand2",
            activebackground=self.COLORS["border"],
            command=self._on_clic_enregistrer,
            state="disabled",
        )
        self.btn_enregistrer.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_supprimer = tk.Button(
            btn_frame,
            text="🗑️ Supprimer la machine",
            font=self.font_small,
            bg=self.COLORS["surface_1"],
            fg=self.COLORS["text_danger"],
            relief="flat",
            bd=1,
            cursor="hand2",
            activebackground=self.COLORS["border"],
            command=self._on_clic_supprimer,
            state="disabled",
        )
        self.btn_supprimer.pack(side=tk.LEFT)

        self.label_message = tk.Label(
            inner_form,
            text="",
            font=self.font_small,
            fg=self.COLORS["text_danger"],
            bg=self.COLORS["surface_2"],
        )
        self.label_message.grid(row=2, column=0, columnspan=4, sticky="w", pady=(6, 0))

        # ----- Section : historique -----
        header_histo = tk.Frame(main, bg=self.COLORS["body_bg"])
        header_histo.pack(fill=tk.X, pady=(0, 6))

        self.label_histo = tk.Label(
            header_histo, text="Historique des événements (toutes machines)",
            font=self.font_medium, fg=self.COLORS["text_primary"], bg=self.COLORS["body_bg"],
        )
        self.label_histo.pack(side=tk.LEFT, anchor=tk.W)

        self.btn_effacer_historique = tk.Button(
            header_histo, text="🗑️ Vider l'historique affiché", font=self.font_small,
            bg=self.COLORS["surface_1"], fg=self.COLORS["text_danger"], relief="flat", bd=1,
            cursor="hand2", activebackground=self.COLORS["border"],
            command=self._on_clic_effacer_historique,
        )
        self.btn_effacer_historique.pack(side=tk.RIGHT)

        self.tree_historique = ttk.Treeview(
            main,
            columns=("heure", "machine", "evenement"),
            show="headings",
            style="Dark.Treeview",
            height=10,
        )
        self.tree_historique.heading("heure", text="Heure")
        self.tree_historique.heading("machine", text="Machine")
        self.tree_historique.heading("evenement", text="Événement")
        self.tree_historique.column("heure", width=140)
        self.tree_historique.column("machine", width=200)
        self.tree_historique.column("evenement", width=150)
        self.tree_historique.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # CHARGEMENT DES DONNÉES
    # ------------------------------------------------------------------

    def _charger_machines(self):
        """Recharge le tableau des machines depuis la BDD."""
        self.tree_machines.delete(*self.tree_machines.get_children())
        for id_m, nom, ip in self.get_machines():
            self.tree_machines.insert("", "end", iid=str(id_m), values=(nom, ip))

    def _charger_historique(self, ip=None):
        """Recharge le tableau d'historique, filtré ou non sur une machine."""
        self.tree_historique.delete(*self.tree_historique.get_children())
        for id_e, heure, ip_evt, nom, evenement in (
            self.get_evenements(ip=ip, limit=100)
            if ip
            else self.get_evenements(limit=100)
        ):
            tag = (
                "danger"
                if "Hors ligne" in evenement or "Erreur" in evenement
                else "success"
            )
            self.tree_historique.insert(
                "", "end", values=(heure, nom, evenement), tags=(tag,)
            )
        self.tree_historique.tag_configure(
            "danger", foreground=self.COLORS["text_danger"]
        )
        self.tree_historique.tag_configure(
            "success", foreground=self.COLORS["text_success"]
        )

    # ------------------------------------------------------------------
    # ÉVÉNEMENTS UI
    # ------------------------------------------------------------------

    def _on_selection_machine(self, event):
        selection = self.tree_machines.selection()
        if not selection:
            self.machine_selectionnee = None
            self.btn_enregistrer.config(state="disabled")
            self.btn_supprimer.config(state="disabled")
            return

        id_m = int(selection[0])
        nom, ip = self.tree_machines.item(selection[0], "values")

        self.machine_selectionnee = id_m
        self.ip_filtre_historique = ip
        self.entry_nom.delete(0, tk.END)
        self.entry_nom.insert(0, nom)
        self.entry_ip.delete(0, tk.END)
        self.entry_ip.insert(0, ip)

        self.btn_enregistrer.config(state="normal")
        self.btn_supprimer.config(state="normal")
        self.label_message.config(text="")

        # Filtre l'historique sur la machine sélectionnée
        self.label_histo.config(text=f"Historique des événements — {nom}")
        self._charger_historique(ip=ip)

    def _on_clic_enregistrer(self):
        if self.machine_selectionnee is None:
            return

        nouveau_nom = self.entry_nom.get().strip()
        nouvelle_ip = self.entry_ip.get().strip()

        if not nouveau_nom or not nouvelle_ip:
            self.label_message.config(text="Le nom et l'IP ne peuvent pas être vides.")
            return

        succes = self.on_modifier(self.machine_selectionnee, nouveau_nom, nouvelle_ip)
        if succes:
            self.label_message.config(text="Modifications enregistrées.", fg=self.COLORS["text_success"])
            self.label_histo.config(text="Historique des événements (toutes machines)")
            self._charger_machines()
            self._charger_historique()
        else:
            self.label_message.config(
                text="Erreur : cette adresse IP est déjà utilisée par une autre machine.",
                fg=self.COLORS["text_danger"],
            )

    
    def _on_clic_effacer_historique(self):
        cible = f"de « {self.entry_nom.get()} »" if self.ip_filtre_historique else "de TOUTES les machines"
        confirme = messagebox.askyesno(
            "Confirmer la suppression",
            f"Voulez-vous vraiment supprimer l'historique {cible} ?\nCette action est irréversible.",
            parent=self,
        )
        if not confirme:
            return
        self.on_effacer_historique(self.ip_filtre_historique)
        self._charger_historique(ip=self.ip_filtre_historique)
        

    def _on_clic_supprimer(self):
        if self.machine_selectionnee is None:
            return

        self.on_supprimer(self.machine_selectionnee)
        self.machine_selectionnee = None
        self.entry_nom.delete(0, tk.END)
        self.entry_ip.delete(0, tk.END)
        self.btn_enregistrer.config(state="disabled")
        self.btn_supprimer.config(state="disabled")
        self.label_message.config(
            text="Machine supprimée.", fg=self.COLORS["text_success"]
        )
        self.label_histo.config(text="Historique des événements (toutes machines)")

        self._charger_machines()
        self._charger_historique()
