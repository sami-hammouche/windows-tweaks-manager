import os
import subprocess
import ctypes
import sys
import tempfile

# Dossier courant : le script parcourt son propre repertoire
DOSSIER = os.path.dirname(os.path.abspath(__file__))
IGNORER = {"opti_manager.py", "launcher.bat"}

# --- Admin ---
def est_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def relancer_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit()

def lire(chemin):
    for enc in ('utf-16', 'utf-8-sig', 'utf-8', 'latin-1'):
        try:
            with open(chemin, 'r', encoding=enc) as f:
                return f.read()
        except Exception:
            continue
    return ""

def scanner():
    reg_files, bat_files = [], []
    for racine, _, noms in os.walk(DOSSIER):
        for nom in sorted(noms):
            if nom in IGNORER: continue
            chemin = os.path.join(racine, nom)
            ext = os.path.splitext(nom)[1].lower()
            if ext == '.reg':
                reg_files.append(chemin)
            elif ext in ('.bat', '.cmd'):
                bat_files.append(chemin)
    return reg_files, bat_files

def appliquer(chemin):
    ext = os.path.splitext(chemin)[1].lower()
    if ext == '.reg':
        subprocess.run(['regedit', '/s', chemin], timeout=30)
    elif ext in ('.bat', '.cmd'):
        # On retire les pause, sinon le script attend une touche indefiniment
        contenu = lire(chemin)
        lignes = [l for l in contenu.splitlines()
                  if l.strip().lower() not in ('pause', '@pause')]
        tmp = tempfile.NamedTemporaryFile(suffix='.bat', delete=False,
                                          mode='w', encoding='utf-8')
        tmp.write('\n'.join(lignes))
        tmp.close()
        subprocess.run(['cmd', '/c', tmp.name],
                       stdin=subprocess.DEVNULL,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       timeout=15)
        os.remove(tmp.name)

if __name__ == '__main__':
    if not est_admin():
        print("Droits administrateur requis, relancement...")
        relancer_admin()

    reg_files, bat_files = scanner()
    fichiers = reg_files + bat_files
    print(f"{len(reg_files)} fichiers .reg et {len(bat_files)} scripts trouves.\n")

    for i, chemin in enumerate(fichiers, 1):
        print(f"({i}/{len(fichiers)})  {os.path.basename(chemin)}")
        try:
            appliquer(chemin)
        except Exception:
            pass

    print("\nOptimisation terminee.")
    input("Appuyez sur Entree pour fermer...")
