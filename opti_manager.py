import os
import subprocess
import ctypes
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import ttk, messagebox

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

def lancer_thread():
    selectionnes = [c for c, var in cases if var.get()]
    if not selectionnes:
        messagebox.showinfo("Info", "Aucun element selectionne.")
        return

    btn.config(state="disabled", text="En cours...")
    barre["maximum"] = len(selectionnes)
    barre["value"] = 0

    def executer():
        total = len(selectionnes)
        for i, chemin in enumerate(selectionnes):
            nom = os.path.basename(chemin)
            fenetre.after(0, lambda a=nom, idx=i:
                lbl_statut.config(text=f"({idx+1}/{total})  {a}")
            )
            try:
                appliquer(chemin)
            except Exception:
                pass
            fenetre.after(0, lambda: barre.step(1))
        fenetre.after(0, termine)

    # Thread demon : l'interface reste utilisable pendant l'execution
    threading.Thread(target=executer, daemon=True).start()

def termine():
    btn.config(state="normal", text="OPTIMISER MON PC")
    lbl_statut.config(text="Termine !")
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

cadre_ext = tk.Frame(fenetre, bg="#f0f0f0")
cadre_ext.pack(fill="both", expand=True, padx=15)

canvas = tk.Canvas(cadre_ext, bg="#f0f0f0", highlightthickness=0)
scrollbar = tk.Scrollbar(cadre_ext, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

cadre_liste = tk.Frame(canvas, bg="#f0f0f0")
canvas.create_window((0, 0), window=cadre_liste, anchor="nw")
cadre_liste.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

cases = []
reg_files, bat_files = scanner()
for chemin in reg_files + bat_files:
    var = tk.BooleanVar(value=True)
    cases.append((chemin, var))
    tk.Checkbutton(cadre_liste, text=os.path.basename(chemin),
                   variable=var, bg="#f0f0f0", anchor="w",
                   font=("Arial", 9), wraplength=530
                   ).pack(fill="x", padx=8, pady=0)

barre = ttk.Progressbar(fenetre, orient="horizontal", mode="determinate", length=580)
barre.pack(padx=15, pady=(15, 2))

lbl_statut = tk.Label(fenetre, text="", font=("Arial", 9, "italic"),
                       bg="#f0f0f0", fg="#555555")
lbl_statut.pack(pady=(0, 5))

btn = tk.Button(fenetre, text="OPTIMISER MON PC",
                font=("Arial", 13, "bold"), bg="green", fg="white",
                padx=20, pady=10, command=lancer_thread)
btn.pack(pady=10)

fenetre.mainloop()
