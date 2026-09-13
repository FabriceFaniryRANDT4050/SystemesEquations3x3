import tkinter as tk
from tkinter import messagebox
import numpy as np

# ---------- Palette de couleurs ----------
BG_COLOR = "#0f172a"       # fond principal (bleu nuit)
CARD_COLOR = "#1e293b"     # carte de saisie (bleu ardoise)
ENTRY_BG = "#334155"       # fond des champs
ACCENT = "#22c55e"         # vert (bouton principal)
ACCENT_HOVER = "#16a34a"   # vert au survol
SECONDARY = "#475569"      # bouton secondaire
SECONDARY_HOVER = "#334155"
TEXT_COLOR = "#e2e8f0"
MUTED_COLOR = "#94a3b8"

FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_SUB = ("Segoe UI", 9)
FONT_ENTRY = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BTN = ("Segoe UI", 10, "bold")
FONT_RESULT = ("Segoe UI", 12, "bold")


def resoudre():
    try:
        # Récupération des valeurs saisies dans les cases
        A = np.array([[float(entries[i][j].get()) for j in range(3)] for i in range(3)])
        B = np.array([float(entries[i][3].get()) for i in range(3)])

        # Calcul de la solution
        X = np.linalg.solve(A, B)
        result_var.set(f"x = {X[0]:.2f}      y = {X[1]:.2f}      z = {X[2]:.2f}")
        result_label.config(fg=ACCENT)

    except ValueError:
        messagebox.showerror("Erreur de saisie", "Veuillez entrer des nombres valides dans toutes les cases.")
    except np.linalg.LinAlgError:
        messagebox.showerror("Erreur mathématique", "Le système n'a pas de solution unique (matrice singulière).")


def effacer():
    for row in entries:
        for e in row:
            e.delete(0, tk.END)
            e.insert(0, "0")
    result_var.set("Entrez les coefficients et cliquez sur Résoudre")
    result_label.config(fg=MUTED_COLOR)


def make_entry(parent, width, highlight):
    return tk.Entry(
        parent, width=width, justify="center", font=FONT_ENTRY,
        bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
        relief="flat", highlightthickness=1.5,
        highlightbackground=highlight, highlightcolor=ACCENT
    )


def bind_hover(widget, normal, hover):
    widget.bind("<Enter>", lambda e: widget.config(bg=hover))
    widget.bind("<Leave>", lambda e: widget.config(bg=normal))


# ---------- Fenêtre principale ----------
root = tk.Tk()
root.title("Solveur de systèmes 3×3")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

window_width, window_height = 640, 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
pos_x = (screen_width - window_width) // 2
pos_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

# ---------- En-tête ----------
tk.Label(root, text="Solveur de systèmes linéaires 3×3", font=FONT_TITLE,
         bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(24, 4))

tk.Label(root, text="Résolution du système  A · X = B", font=FONT_SUB,
         bg=BG_COLOR, fg=MUTED_COLOR).pack(pady=(0, 18))

# ---------- Carte de saisie ----------
card = tk.Frame(root, bg=CARD_COLOR, padx=18, pady=18, highlightthickness=1,
                highlightbackground="#334155")
card.pack(padx=24, fill="x")

entries = []
var_labels = ["x", "y", "z"]

for i in range(3):
    row_frame = tk.Frame(card, bg=CARD_COLOR)
    row_frame.pack(pady=6)
    row_entries = []

    for j in range(3):
        e = make_entry(row_frame, width=5, highlight="#475569")
        e.pack(side="left", padx=3)
        e.insert(0, "0")
        row_entries.append(e)

        suffix = "  +" if j < 2 else "  ="
        tk.Label(row_frame, text=f"{var_labels[j]}{suffix}", font=FONT_LABEL,
                 bg=CARD_COLOR, fg=TEXT_COLOR, width=3, anchor="w").pack(side="left", padx=(2, 4))

    e_b = make_entry(row_frame, width=6, highlight=ACCENT)
    e_b.pack(side="left", padx=3)
    e_b.insert(0, "0")
    row_entries.append(e_b)

    entries.append(row_entries)

# ---------- Boutons ----------
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=20)

btn_resoudre = tk.Button(
    btn_frame, text="Résoudre", command=resoudre, bg=ACCENT, fg="white",
    font=FONT_BTN, relief="flat", padx=22, pady=7, borderwidth=0,
    activebackground=ACCENT_HOVER, activeforeground="white", cursor="hand2"
)
btn_resoudre.pack(side="left", padx=6)
bind_hover(btn_resoudre, ACCENT, ACCENT_HOVER)

btn_effacer = tk.Button(
    btn_frame, text="Effacer", command=effacer, bg=SECONDARY, fg="white",
    font=FONT_BTN, relief="flat", padx=22, pady=7, borderwidth=0,
    activebackground=SECONDARY_HOVER, activeforeground="white", cursor="hand2"
)
btn_effacer.pack(side="left", padx=6)
bind_hover(btn_effacer, SECONDARY, SECONDARY_HOVER)

# ---------- Résultat ----------
result_var = tk.StringVar(value="Entrez les coefficients et cliquez sur Résoudre")
result_label = tk.Label(root, textvariable=result_var, font=FONT_RESULT,
                         bg=BG_COLOR, fg=MUTED_COLOR, wraplength=400, justify="center")
result_label.pack(pady=(4, 20))

root.mainloop()