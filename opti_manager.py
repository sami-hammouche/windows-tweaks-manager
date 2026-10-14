import os
import subprocess
import ctypes
import sys
import tempfile
import tkinter as tk
from tkinter import messagebox

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

def lancer():
    selectionnes = [c for c, var in cases if var.get()]
    if not selectionnes:
        messagebox.showinfo("Info", "Aucun element selectionne.")
        return
    btn.config(state="disabled", text="En cours...")
    fenetre.update()
    for chemin in selectionnes:
        try:
            appliquer(chemin)
        except Exception:
            pass
    btn.config(state="normal", text="OPTIMISER MON PC")
    messagebox.showinfo("Termine", "Optimisation terminee !")

if not est_admin():
    res = ctypes.windll.user32.MessageBoxW(0,
        "Relancer en administrateur ? (necessaire pour les .reg)",
        "Droits requis", 0x24)
    if res == 6: relancer_admin()
    sys.exit()

# --- Interface ---
fenetre = tk.Tk()
fenetre.title("PACK OPTI")
fenetre.geometry("620x680")
fenetre.configure(bg="#f0f0f0")
fenetre.resizable(False, False)

tk.Label(fenetre, text="PACK OPTI - Optimisation PC",
         font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

cadre_liste = tk.Frame(fenetre, bg="#f0f0f0")
cadre_liste.pack(fill="both", expand=True, padx=15)

cases = []
reg_files, bat_files = scanner()
for chemin in reg_files + bat_files:
    var = tk.BooleanVar(value=True)
    cases.append((chemin, var))
    tk.Checkbutton(cadre_liste, text=os.path.basename(chemin),
                   variable=var, bg="#f0f0f0", anchor="w",
                   font=("Arial", 9), wraplength=530
                   ).pack(fill="x", padx=8, pady=0)

btn = tk.Button(fenetre, text="OPTIMISER MON PC",
                font=("Arial", 13, "bold"), bg="green", fg="white",
                padx=20, pady=10, command=lancer)
btn.pack(pady=10)

fenetre.mainloop()
