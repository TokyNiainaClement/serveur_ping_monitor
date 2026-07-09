import subprocess
import platform


def ping(ip):
    """Ping une IP une fois, retourne True si elle répond."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    commande = ["ping", param, "1", ip]
    try:
        resultat = subprocess.run(
            commande, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3
        )
        return resultat.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def ping_toutes_les_machines(db):
    """Ping chaque machine de la base et enregistre le résultat dans evenements."""
    machines = db.get_machines()
    for id_m, nom, ip in machines:
        actif = ping(ip)
        evenement = "UP" if actif else "DOWN"
        db.add_evenement(ip, nom, evenement)
        print(f"[{evenement}] {nom} ({ip})")
