import os
import subprocess
import ctypes
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import ttk, messagebox

if getattr(sys, 'frozen', False):
    DOSSIER = sys._MEIPASS
else:
    DOSSIER = os.path.dirname(os.path.abspath(__file__))
IGNORER = {"opti_manager.py", "launcher.bat"}

# Noms affichés pour chaque fichier
NOMS = {
    # --- Registre ---
    "1 - keyboard Optimization.reg":                                     "Optimisation clavier #1",
    "2 - keyboard Optimization.reg":                                     "Optimisation clavier #2",
    "3 - Keyboard Optimization.reg":                                     "Optimisation clavier #3",
    "4 - Keyboard Optimization.reg":                                     "Optimisation clavier #4",
    "5 - Keyboard Optimization.reg":                                     "Optimisation clavier #5",
    "6 - Keyboard Optimization.reg":                                     "Optimisation clavier #6",
    "7 - Keyboard Optimization.reg":                                     "Optimisation clavier #7",
    "8 - Keyboard Optimization.reg":                                     "Optimisation clavier #8",
    "9 - Keyboard Optimization.reg":                                     "Optimisation clavier #9",
    "10 - Keyboard Optimization.reg":                                    "Optimisation clavier #10",
    "11 - Keyboard Optimization.reg":                                    "Optimisation clavier #11",
    "1 Unpark All CPU Cores.reg":                                        "Déparquage de tous les cœurs CPU",
    "1. DisableEnergyEstimation.reg":                                    "Désactiver estimation d'énergie",
    "1. Memory Management Optimizations (Credit EverythingTech).reg":    "Optimisation gestion mémoire",
    "1. Registry Tweaks.reg":                                            "Tweaks registre #1",
    "1.reg":                                                             "Tweaks divers #1",
    "2. Disable LargeSystemCache.reg":                                   "Désactiver LargeSystemCache",
    "2. DisableEnergyLogging.reg":                                       "Désactiver journalisation énergie",
    "2. Extra Registry Tweaks.reg":                                      "Tweaks registre supplémentaires",
    "2.reg":                                                             "Tweaks divers #2",
    "3 Disable Spectre _ Meltdown Windows Patches.reg":                  "Désactiver patches Spectre / Meltdown",
    "3. DisableCpuPwrThrottling.reg":                                    "Désactiver la limitation de puissance CPU",
    "3.reg":                                                             "Tweaks divers #3",
    "4.reg":                                                             "Tweaks divers #4",
    "5 Disable UAC.reg":                                                 "Désactiver l'UAC",
    "5.reg":                                                             "Tweaks divers #5",
    "8. Disable File History Service.reg":                               "Désactiver l'historique des fichiers",
    "9. Large system cache.reg":                                         "Activer le cache système étendu",
    "cpu.reg":                                                           "Optimisation CPU",
    "cpuBySqo&Hzk 1.reg":                                               "Tweaks CPU avancés #1",
    "cpuBySqo&Hzk 2.reg":                                               "Tweaks CPU avancés #2",
    "cpuBySqo&Hzk 3.reg":                                               "Tweaks CPU avancés #3",
    "cpuBySqo&Hzk 4.reg":                                               "Tweaks CPU avancés #4",
    "cpuBySqo&Hzk 5.reg":                                               "Tweaks CPU avancés #5",
    "csrss.exe priority pour moins d_input lag.reg":                     "Priorité CSRSS — Réduction input lag",
    "Decrease Delay.reg":                                                "Réduction des délais système",
    "Desac_MPO.reg":                                                     "Désactiver MPO (Multi-Plane Overlay)",
    "Disable Game Bar.reg":                                              "Désactiver la barre de jeu Xbox",
    "Disable Hibernate.reg":                                             "Désactiver la mise en veille prolongée",
    "DisablePageCombining.REG":                                          "Désactiver la combinaison de pages mémoire",
    "DisableWriteCombining.reg":                                         "Désactiver la combinaison d'écriture mémoire",
    "Disable_Preemption.reg":                                            "Désactiver la préemption GPU",
    "DmaRemapping.reg":                                                  "Configuration DMA Remapping",
    "Désactive buffer list tracking.reg":                                "Désactiver le suivi de liste buffer",
    "Désactive le démarrage rapide (allège la RAM et le CPU).reg":       "Désactiver le démarrage rapide Windows",
    "Désactive VBS.reg":                                                 "Désactiver VBS (sécurité par virtualisation)",
    "Désactive.reg":                                                     "Désactivations diverses",
    "Désactiver Cortana.reg":                                            "Désactiver Cortana",
    "Désactiver HAGS.reg":                                               "Désactiver HAGS (planification GPU)",
    "Désactiver Mode Jeu.reg":                                           "Désactiver le mode jeu Windows",
    "Désactiver Prefetech.reg":                                          "Désactiver Prefetch",
    "Exclusive_Fullscreen.reg":                                          "Forcer le plein écran exclusif",
    "Fix Keyboard Input Delay.reg":                                      "Corriger le délai d'entrée clavier",
    "Game Priority Optimizations.reg":                                   "Optimisation priorité des jeux",
    "GameBare off.reg":                                                  "Désactiver Game DVR / enregistrement",
    "gpu.reg":                                                           "Optimisation GPU",
    "GpuEnergyDriver.reg":                                               "Configuration driver énergie GPU",
    "High Priority Fortnite.reg":                                        "Haute priorité CPU pour Fortnite",
    "input lag optimisation.reg":                                        "Réduction de l'input lag",
    "K.reg":                                                             "Tweaks clavier K",
    "K2.reg":                                                            "Tweaks clavier K2",
    "KeyBoard Revert Optimization.reg":                                  "Restauration optimisation clavier",
    "LowLatencyScaling.reg":                                             "Mise à l'échelle basse latence",
    "memort booster reg.reg":                                            "Boost mémoire RAM",
    "Memory Management Optimizations.reg":                               "Optimisation avancée de la mémoire",
    "network.reg":                                                       "Optimisation réseau",
    "Optimisation Game Priority.reg":                                    "Priorité CPU — Mode jeu",
    "Optimize ALL Windows Settings.reg":                                 "Optimiser tous les paramètres Windows",
    "Paging Drivers To SSD (Disable).REG":                              "Désactiver pagination drivers vers SSD",
    "Power Optimizations.reg":                                           "Optimisation plan d'alimentation",
    "Prioritys.reg":                                                     "Priorités des processus système",
    "RayOptimizer.reg":                                                  "Optimisation Ray Tracing",
    "res fix.reg":                                                       "Correctif de résolution",
    "speed boost.reg":                                                   "Boost vitesse système global",
    "Transactional Synchronization Extensions.reg":                      "Activer extensions TSX",
    "Tweaked CRSS.reg":                                                  "CSRSS optimisé",
    "Tweaked CSRSS Priority.reg":                                        "Priorité CSRSS optimisée",
    "Tweaked lsass Priority.reg":                                        "Priorité LSASS optimisée",
    "Tweaked winlogon Priority.reg":                                     "Priorité Winlogon optimisée",
    "Unhide Silksmoothness.reg":                                         "Activer SilkSmoothness",
    "USB Suspend Disable.reg":                                           "Désactiver la suspension USB",
    # --- Scripts ---
    "2 Clear DNS Cache (Ping Improve).cmd":                              "Vider le cache DNS (améliore le ping)",
    "5 Delete Log Files.bat":                                            "Supprimer les fichiers logs",
    "6 Delete Temporary Files.bat":                                      "Supprimer les fichiers temporaires",
    "7 Delete Windows Update Cache.cmd":                                 "Vider le cache Windows Update",
    "cleaner.bat":                                                       "Nettoyage système complet",
    "Delete Log Files.cmd":                                              "Supprimer les logs système",
    "Delete Temporary Files.cmd":                                        "Supprimer les fichiers temp",
    "Delete Update Cache.cmd":                                           "Vider le cache des mises à jour",
    "Disable USB Devices Idle.bat":                                      "Désactiver la mise en veille des USB",
    "Disable USB Powersaving.bat":                                       "Désactiver l'économie d'énergie USB",
    "opti clavier (1).bat":                                              "Optimisation clavier (script)",
    "OptiBooster (2).bat":                                               "OptiBooster — Boost système",
}

def nom_affiche(chemin):
    nom = os.path.basename(chemin)
    return NOMS.get(nom, nom)

# --- Admin ---
def est_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def relancer_admin():
    if getattr(sys, 'frozen', False):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, None, None, 1)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit()

if not est_admin():
    res = ctypes.windll.user32.MessageBoxW(0,
        "Relancer en administrateur ? (necessaire pour les .reg)",
        "Droits requis", 0x24)
    if res == 6: relancer_admin()
    sys.exit()

def lire(chemin):
    for enc in ('utf-16', 'utf-8-sig', 'utf-8', 'latin-1'):
        try:
            with open(chemin, 'r', encoding=enc) as f:
                return f.read()
        except Exception:
            continue
    return ""

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
            affiche = nom_affiche(chemin)
            ext = os.path.splitext(chemin)[1].lower()

            fenetre.after(0, lambda a=affiche, idx=i:
                lbl_statut.config(text=f"({idx+1}/{total})  {a}")
            )

            try:
                if ext == '.reg':
                    subprocess.run(['regedit', '/s', chemin], timeout=30)

                elif ext in ('.bat', '.cmd'):
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

                elif ext == '.exe':
                    subprocess.Popen([chemin]).wait()

            except Exception:
                pass

            fenetre.after(0, lambda: barre.step(1))

        fenetre.after(0, termine)

    threading.Thread(target=executer, daemon=True).start()

def termine():
    btn.config(state="normal", text="OPTIMISER MON PC")
    lbl_statut.config(text="Termine !")
    messagebox.showinfo("Termine", "Optimisation terminee !")

def scanner():
    reg_files, bat_files = [], []
    for racine, _, noms in os.walk(DOSSIER):
        for nom in sorted(noms):
            if nom in IGNORER: continue
            chemin = os.path.join(racine, nom)
            ext = os.path.splitext(nom)[1].lower()
            if ext == '.reg':
                reg_files.append(chemin)
            elif ext in ('.bat', '.cmd', '.exe'):
                bat_files.append(chemin)
    return reg_files, bat_files

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

def ajouter_section(titre, fichiers, couleur):
    tk.Label(cadre_liste, text=titre, font=("Arial", 10, "bold"),
             bg=couleur, fg="white", anchor="w", padx=8, pady=3
             ).pack(fill="x", pady=(8, 1))
    for chemin in fichiers:
        var = tk.BooleanVar(value=True)
        cases.append((chemin, var))
        tk.Checkbutton(cadre_liste, text=nom_affiche(chemin),
                       variable=var, bg="#f0f0f0", anchor="w",
                       font=("Arial", 9), wraplength=530
                       ).pack(fill="x", padx=8, pady=0)

reg_files, bat_files = scanner()
ajouter_section(f"  Registre (.reg)  [{len(reg_files)} fichiers]", reg_files, "#1565c0")
ajouter_section(f"  Scripts (.bat/.cmd/.exe)  [{len(bat_files)} fichiers]", bat_files, "#2e7d32")

cadre_btns = tk.Frame(fenetre, bg="#f0f0f0")
cadre_btns.pack(pady=(6, 0))
tk.Button(cadre_btns, text="Tout cocher",
          command=lambda: [v.set(True) for _, v in cases],
          font=("Arial", 9), padx=10).pack(side="left", padx=5)
tk.Button(cadre_btns, text="Tout decocher",
          command=lambda: [v.set(False) for _, v in cases],
          font=("Arial", 9), padx=10).pack(side="left", padx=5)

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
