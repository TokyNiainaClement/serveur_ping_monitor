class Machine:
    """Entité représentant une machine surveillée."""

    def __init__(self, id=None, nom="", ip=""):
        self.id = id
        self.nom = nom
        self.ip = ip

    def __repr__(self):
        return f"Machine(id={self.id}, nom='{self.nom}', ip='{self.ip}')"

    @staticmethod
    def from_row(row):
        """Construit une Machine à partir d'une ligne SQLite (id, nom, ip)."""
        return Machine(id=row[0], nom=row[1], ip=row[2])
