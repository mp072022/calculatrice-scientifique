# -*- coding: utf-8 -*-
"""
Calculatrice scientifique — Windows, interface moderne et TRES PERSONNALISABLE
================================================================================

Aucune installation en plus de Python : bibliotheque standard seulement
(tkinter + math + json).

Pour la lancer :
    1. Installe Python 3 depuis python.org (coche "Add python.exe to PATH").
    2. Double-clique sur ce fichier, ou : python calculatrice-scientifique.py

Pour en faire un .exe :
    pip install pyinstaller
    pyinstaller --onefile --windowed --name "Calculatrice-scientifique" calculatrice-scientifique.py

MODES (bouton en haut a gauche, ou Ctrl+M) :
    - Mode Normal : seulement les touches de base
      (chiffres, + - x /, virgule, =, C, fleche, parentheses),
      fenetre plus petite et plus simple.
    - Mode Scientifique : toutes les fonctions
      (sin, cos, tan, log, ln, racines, puissances, factorielle,
      pi, e, memoire MC/MR/M+/M-/MS, 2nd, DEG/RAD).
    Le mode choisi est sauvegarde et retrouve au demarrage.

PERSONNALISATION (bouton "Personnaliser" en haut) :
    - 8 themes prets : Sombre, Clair, Bleu nuit, Vert foret, Violet,
      Orange coucher de soleil, Rose, Noir pur (OLED)
    - Couleurs libres : fond, boutons chiffres, boutons fonctions,
      bouton =, texte, texte secondaire, panneau historique
      -> choisis n'importe quelle couleur avec la palette Windows
    - Police : Segoe UI, Arial, Verdana, Consolas, Tahoma
    - Tailles : affichage (20 a 48), boutons (10 a 20), espacement
    - Style des boutons : Plat, Relief leger, Avec bordure
    - Fenetre : Petite / Moyenne / Grande / Tres grande,
      toujours au premier plan, transparence reglable
    - Affichage : historique visible ou cache, nombre de decimales,
      separateur virgule ou point, separateur de milliers oui/non
    - Comportement : DEG ou RAD au demarrage, garder l'historique
      entre les sessions oui/non
    - Tout est sauvegarde automatiquement dans calculatrice_config.json
      (a cote du .py / du .exe) et recharge au prochain demarrage.
    - Bouton "Reinitialiser tout" pour revenir comme au debut.

Fonctions de calcul (inchangees) :
    + - x / % parentheses, sin cos tan (+ inverses avec 2nd),
    log, ln, racine, x2, x^y, 1/x, |x|, factorielle, pi, e,
    DEG/RAD, memoire MC MR M+ M- MS, historique cliquable, clavier complet.

Bouton = repete : appuyer plusieurs fois sur = repete la derniere
    operation (+, -, x, /). Exemple : 9+9 = 18, = donne 27, = donne 36.
"""

import json
import math
import os
import re
import sys
import tkinter as tk
from tkinter import colorchooser, messagebox

# ----------------------------------------------------------------------
# Fichier de reglages (a cote du .py, ou du .exe si compile)
# ----------------------------------------------------------------------
def _config_path():
    try:
        base = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) \
            else os.path.dirname(os.path.abspath(__file__))
    except Exception:
        base = os.path.expanduser("~")
    return os.path.join(base, "calculatrice_config.json")


CONFIG_PATH = _config_path()

THEMES = {
    "sombre": {"bg": "#202020", "panel": "#2b2b2b", "btn": "#323232",
        "btn_hover": "#3d3d3d", "op": "#2b2b2b", "op_hover": "#3d3d3d",
        "accent": "#4cc2ff", "equals": "#4cc2ff", "equals_hover": "#6fd0ff",
        "equals_text": "#003a5c", "text": "#ffffff", "subtext": "#a3a3a3"},
    "clair": {"bg": "#f3f3f3", "panel": "#ffffff", "btn": "#ffffff",
        "btn_hover": "#e7e7e7", "op": "#f9f9f9", "op_hover": "#ececec",
        "accent": "#0067c0", "equals": "#0067c0", "equals_hover": "#1975c5",
        "equals_text": "#ffffff", "text": "#1b1b1b", "subtext": "#5d5d5d"},
    "bleu": {"bg": "#0f1e38", "panel": "#16294d", "btn": "#1d3560",
        "btn_hover": "#28477e", "op": "#16294d", "op_hover": "#223a68",
        "accent": "#38bdf8", "equals": "#0284c7", "equals_hover": "#0ea5e9",
        "equals_text": "#ffffff", "text": "#e0f2fe", "subtext": "#93b8d8"},
    "vert": {"bg": "#12261a", "panel": "#1a3524", "btn": "#22452f",
        "btn_hover": "#2d5a3f", "op": "#1a3524", "op_hover": "#254730",
        "accent": "#4ade80", "equals": "#16a34a", "equals_hover": "#22c55e",
        "equals_text": "#ffffff", "text": "#dcfce7", "subtext": "#8fbc9f"},
    "violet": {"bg": "#241433", "panel": "#331d47", "btn": "#42265e",
        "btn_hover": "#553374", "op": "#331d47", "op_hover": "#452a5e",
        "accent": "#c084fc", "equals": "#9333ea", "equals_hover": "#a855f7",
        "equals_text": "#ffffff", "text": "#f3e8ff", "subtext": "#b79fd1"},
    "orange": {"bg": "#2b1a10", "panel": "#3d2415", "btn": "#4f2f1b",
        "btn_hover": "#663d24", "op": "#3d2415", "op_hover": "#52301c",
        "accent": "#fb923c", "equals": "#ea580c", "equals_hover": "#f97316",
        "equals_text": "#ffffff", "text": "#ffedd5", "subtext": "#c9a07a"},
    "rose": {"bg": "#2e1220", "panel": "#421a2e", "btn": "#55223c",
        "btn_hover": "#6e2d4f", "op": "#421a2e", "op_hover": "#57253c",
        "accent": "#f472b6", "equals": "#db2777", "equals_hover": "#ec4899",
        "equals_text": "#ffffff", "text": "#fce7f3", "subtext": "#c48aa6"},
    "noir": {"bg": "#000000", "panel": "#0a0a0a", "btn": "#141414",
        "btn_hover": "#222222", "op": "#0a0a0a", "op_hover": "#1a1a1a",
        "accent": "#ffffff", "equals": "#ffffff", "equals_hover": "#e5e5e5",
        "equals_text": "#000000", "text": "#ffffff", "subtext": "#888888"},
}
THEME_LABELS = {"sombre": "Sombre", "clair": "Clair", "bleu": "Bleu nuit",
    "vert": "Vert foret", "violet": "Violet", "orange": "Orange",
    "rose": "Rose", "noir": "Noir pur (OLED)"}
WINDOW_SIZES = {"petite": "640x480", "moyenne": "760x560",
    "grande": "900x650", "tres_grande": "1050x750",
    "normale_petite": "420x520", "normale_moyenne": "480x600"}
COLOR_LABELS = {"bg": "Fond de la fenetre", "panel": "Panneau historique",
    "btn": "Boutons chiffres", "op": "Boutons fonctions / operateurs",
    "equals": "Bouton = (accent)", "text": "Texte principal",
    "subtext": "Texte secondaire"}

DEFAULT_SETTINGS = {
    "theme_name": "sombre", "custom_colors": {},
    "font_family": "Segoe UI", "display_size": 30, "button_size": 13,
    "spacing": 2, "button_style": "plat", "window_size": "moyenne",
    "always_on_top": False, "opacity": 1.0, "show_history": True,
    "decimals": 10, "decimal_sep": ",", "thousands_sep": False,
    "default_degrees": True, "keep_history": False,
    "mode": "scientifique", "saved_history": [],
}


def load_settings():
    s = dict(DEFAULT_SETTINGS)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            s.update({k: v for k, v in data.items() if k in s})
    except Exception:
        pass
    return s


def save_settings(s):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(s, f, ensure_ascii=False, indent=2)
    except Exception:
        pass



class Calculatrice(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.title("Calculatrice scientifique")
        self.minsize(380, 440)
        self.expression = ""
        self.just_evaluated = False
        self.last_op = None
        self.last_operand = None
        self.degrees = bool(self.settings["default_degrees"])
        self.second = False
        self.memory = 0.0
        self.mode = self.settings.get("mode", "scientifique")
        if self.mode not in ("scientifique", "normal"):
            self.mode = "scientifique"
        self._build_ui()
        self._apply_all(save=False)
        if self.settings.get("keep_history"):
            for entry in self.settings.get("saved_history", []):
                self.hist_items.append(entry)
                self.history.insert("end", entry)
        self.bind("<Key>", self._on_key)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _colors(self):
        c = dict(THEMES.get(self.settings["theme_name"], THEMES["sombre"]))
        c.update(self.settings.get("custom_colors") or {})
        # derive hover/accent variants if accent was customised alone
        c.setdefault("btn_hover", c["btn"])
        c.setdefault("op_hover", c["op"])
        c["accent"] = c.get("equals", c.get("accent", "#4cc2ff"))
        c["equals_hover"] = c.get("equals_hover", c["equals"])
        c["equals_text"] = c.get("equals_text", "#ffffff")
        return c

    def _on_close(self):
        if self.settings.get("keep_history"):
            self.settings["saved_history"] = self.hist_items[-100:]
        self.settings["mode"] = self.mode
        self.settings["default_degrees"] = self.degrees
        save_settings(self.settings)
        self.destroy()

    # ---------------- Interface ----------------
    def _build_ui(self):
        top = tk.Frame(self)
        top.pack(fill="x", padx=16, pady=(12, 4))
        self.top_frame = top
        bar = tk.Frame(top)
        bar.pack(fill="x", side="top")
        self.bar_frame = bar
        self.mode_btn = tk.Button(bar, bd=0, cursor="hand2",
            font=("Segoe UI", 10, "bold"), command=self._toggle_mode)
        self.mode_btn.pack(side="left")
        self.settings_btn = tk.Button(bar, text="Personnaliser",
            bd=0, cursor="hand2", font=("Segoe UI", 10),
            command=self._open_settings)
        self.settings_btn.pack(side="right")
        self.theme_btn = tk.Button(bar, text="Theme", bd=0, cursor="hand2",
            font=("Segoe UI", 10), command=self._cycle_theme)
        self.theme_btn.pack(side="right", padx=(0, 6))
        self.expr_label = tk.Label(top, text="", anchor="e",
                                   font=("Segoe UI", 13))
        self.expr_label.pack(fill="x", side="top")
        self.display = tk.Label(top, text="0", anchor="e", wraplength=560,
                                font=("Segoe UI Semibold", 30))
        self.display.pack(fill="x", side="top")
        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=12, pady=8)
        self.body_frame = body
        self.pad_sci = tk.Frame(body)
        self.pad_basic = tk.Frame(body)
        hist = tk.Frame(body, width=190)
        hist.pack(side="right", fill="y", padx=(10, 0))
        hist.pack_propagate(False)
        self.hist_frame = hist
        tk.Label(hist, text="Historique", anchor="w",
                 font=("Segoe UI Semibold", 11)).pack(fill="x")
        self.history = tk.Listbox(hist, bd=0, highlightthickness=0,
            activestyle="none", font=("Segoe UI", 10), exportselection=False)
        self.history.pack(fill="both", expand=True, pady=6)
        self.history.bind("<<ListboxSelect>>", self._history_click)
        self.hist_items = []
        self.clear_hist_btn = tk.Button(hist, text="Effacer l'historique",
            bd=0, cursor="hand2", font=("Segoe UI", 9),
            command=self._clear_history)
        self.clear_hist_btn.pack(fill="x")
        self._build_sci_buttons()
        self._build_basic_buttons()

    def _make_btn(self, parent, row, col, text, cmd, kind="num", colspan=1):
        b = tk.Button(parent, text=text, command=cmd, bd=0, cursor="hand2",
                      font=("Segoe UI", 13), activebackground="#888888")
        b.grid(row=row, column=col, columnspan=colspan, sticky="nsew",
               padx=2, pady=2)
        b.kind = kind
        return b

    def _build_sci_buttons(self):
        pad = self.pad_sci
        for i in range(6):
            pad.columnconfigure(i, weight=1)
        for i in range(7):
            pad.rowconfigure(i, weight=1)
        self.buttons = []

        def B(r, c, text, cmd, kind="num"):
            b = self._make_btn(pad, r, c, text, cmd, kind)
            self.buttons.append(b)
            return b
        B(0, 0, "MC", self._mem_clear, "mem")
        B(0, 1, "MR", self._mem_recall, "mem")
        B(0, 2, "M+", self._mem_add, "mem")
        B(0, 3, "M-", self._mem_sub, "mem")
        B(0, 4, "MS", self._mem_store, "mem")
        self.deg_btn = B(0, 5, "DEG" if self.degrees else "RAD",
                         self._toggle_deg, "mem")
        self.second_btn = B(1, 0, "2nd", self._toggle_second, "op")
        B(1, 1, "π", lambda: self._insert("π"), "op")
        B(1, 2, "e", lambda: self._insert("e"), "op")
        B(1, 3, "C", self._clear, "op")
        B(1, 4, "←", self._backspace, "op")
        B(1, 5, "÷", lambda: self._insert("÷"), "op")
        self.btn_sqrt = B(2, 0, "√x", lambda: self._unary("sqrt"), "op")
        B(2, 1, "(", lambda: self._insert("("), "op")
        B(2, 2, ")", lambda: self._insert(")"), "op")
        B(2, 3, "n!", self._factorial, "op")
        B(2, 4, "xʸ", lambda: self._insert("^"), "op")
        B(2, 5, "×", lambda: self._insert("×"), "op")
        self.btn_sin = B(3, 0, "sin", lambda: self._func("sin"), "op")
        B(3, 1, "7", lambda: self._insert("7"))
        B(3, 2, "8", lambda: self._insert("8"))
        B(3, 3, "9", lambda: self._insert("9"))
        B(3, 4, "x²", lambda: self._unary("square"), "op")
        B(3, 5, "−", lambda: self._insert("−"), "op")
        self.btn_cos = B(4, 0, "cos", lambda: self._func("cos"), "op")
        B(4, 1, "4", lambda: self._insert("4"))
        B(4, 2, "5", lambda: self._insert("5"))
        B(4, 3, "6", lambda: self._insert("6"))
        B(4, 4, "1/x", lambda: self._unary("inv"), "op")
        B(4, 5, "+", lambda: self._insert("+"), "op")
        self.btn_tan = B(5, 0, "tan", lambda: self._func("tan"), "op")
        B(5, 1, "1", lambda: self._insert("1"))
        B(5, 2, "2", lambda: self._insert("2"))
        B(5, 3, "3", lambda: self._insert("3"))
        B(5, 4, "|x|", lambda: self._unary("abs"), "op")
        self.equals_btn = B(5, 5, "=", self._equals, "equals")
        self.btn_ln = B(6, 0, "ln", lambda: self._func("ln"), "op")
        B(6, 1, "+/-", self._negate, "op")
        B(6, 2, "0", lambda: self._insert("0"))
        B(6, 3, ",", lambda: self._insert(","), "op")
        self.btn_log = B(6, 4, "log", lambda: self._func("log"), "op")
        B(6, 5, "exp", lambda: self._insert("×10^("), "op")

    def _build_basic_buttons(self):
        """Mode normal : seulement les touches de base."""
        pad = self.pad_basic
        for i in range(4):
            pad.columnconfigure(i, weight=1)
        for i in range(5):
            pad.rowconfigure(i, weight=1)
        self.basic_buttons = []

        def B(r, c, text, cmd, kind="num"):
            b = self._make_btn(pad, r, c, text, cmd, kind)
            self.basic_buttons.append(b)
            return b
        B(0, 0, "C", self._clear, "op")
        B(0, 1, "(", lambda: self._insert("("), "op")
        B(0, 2, ")", lambda: self._insert(")"), "op")
        B(0, 3, "÷", lambda: self._insert("÷"), "op")
        B(1, 0, "7", lambda: self._insert("7"))
        B(1, 1, "8", lambda: self._insert("8"))
        B(1, 2, "9", lambda: self._insert("9"))
        B(1, 3, "×", lambda: self._insert("×"), "op")
        B(2, 0, "4", lambda: self._insert("4"))
        B(2, 1, "5", lambda: self._insert("5"))
        B(2, 2, "6", lambda: self._insert("6"))
        B(2, 3, "−", lambda: self._insert("−"), "op")
        B(3, 0, "1", lambda: self._insert("1"))
        B(3, 1, "2", lambda: self._insert("2"))
        B(3, 2, "3", lambda: self._insert("3"))
        B(3, 3, "+", lambda: self._insert("+"), "op")
        B(4, 0, "←", self._backspace, "op")
        B(4, 1, "0", lambda: self._insert("0"))
        B(4, 2, ",", lambda: self._insert(","), "op")
        self.basic_equals = B(4, 3, "=", self._equals, "equals")

    # ---------------- Modes normal / scientifique ----------------
    def _toggle_mode(self):
        self.mode = "normal" if self.mode == "scientifique" else "scientifique"
        self.settings["mode"] = self.mode
        self._apply_all()

    def _apply_mode(self):
        if self.mode == "scientifique":
            self.pad_basic.pack_forget()
            self.pad_sci.pack(side="left", fill="both", expand=True)
            self.title("Calculatrice scientifique")
            self.mode_btn.configure(text="Mode : Scientifique  ▸  Normal")
        else:
            self.pad_sci.pack_forget()
            self.pad_basic.pack(side="left", fill="both", expand=True)
            self.title("Calculatrice")
            self.mode_btn.configure(text="Mode : Normal  ▸  Scientifique")
        # Fenetre plus etroite en mode normal
        size = self.settings.get("window_size", "moyenne")
        if self.mode == "normal":
            geo = WINDOW_SIZES.get("normale_" + size,
                                   WINDOW_SIZES["normale_moyenne"])
        else:
            geo = WINDOW_SIZES.get(size, WINDOW_SIZES["moyenne"])
        try:
            self.geometry(geo)
        except Exception:
            pass

    # ---------------- Application des reglages ----------------
    def _apply_all(self, save=True):
        s = self.settings
        t = self._colors()
        fam = s.get("font_family", "Segoe UI")
        bsize = int(s.get("button_size", 13))
        sp = int(s.get("spacing", 2))
        style = s.get("button_style", "plat")
        relief = {"plat": "flat", "relief": "raised",
                  "bordure": "groove"}.get(style, "flat")
        bd = 0 if style == "plat" else 2
        self.configure(bg=t["bg"])
        try:
            self.attributes("-topmost", bool(s.get("always_on_top")))
            self.attributes("-alpha", float(s.get("opacity", 1.0)))
        except Exception:
            pass
        for fr in (self.top_frame, self.bar_frame, self.body_frame,
                   self.pad_sci, self.pad_basic, self.hist_frame):
            fr.configure(bg=t["bg"])
        self.expr_label.configure(bg=t["bg"], fg=t["subtext"],
                                  font=(fam, 13))
        self.display.configure(bg=t["bg"], fg=t["text"],
            font=(fam, int(s.get("display_size", 30)), "bold"))
        for btn in (self.mode_btn, self.settings_btn, self.theme_btn):
            btn.configure(bg=t["panel"], fg=t["text"],
                          activebackground=t["op_hover"], font=(fam, 10))
        self.mode_btn.configure(font=(fam, 10, "bold"))
        self.theme_btn.configure(
            text="Theme : " + THEME_LABELS.get(s["theme_name"], "Sombre"))
        if s.get("show_history", True):
            if not self.hist_frame.winfo_ismapped():
                self.hist_frame.pack(side="right", fill="y", padx=(10, 0))
        else:
            self.hist_frame.pack_forget()
        for w in self.hist_frame.winfo_children():
            if isinstance(w, tk.Label):
                w.configure(bg=t["bg"], fg=t["text"], font=(fam, 11, "bold"))
        self.history.configure(bg=t["panel"], fg=t["text"],
            selectbackground=t["equals"], selectforeground=t["equals_text"],
            font=(fam, 10))
        self.clear_hist_btn.configure(bg=t["btn"], fg=t["text"],
                                      font=(fam, 9))
        for b in self.buttons + self.basic_buttons:
            b.configure(font=(fam, bsize), relief=relief, bd=bd,
                        padx=sp, pady=sp)
            if b.kind == "equals":
                b.configure(bg=t["equals"], fg=t["equals_text"],
                            activebackground=t["equals_hover"])
            elif b.kind in ("op", "mem"):
                b.configure(bg=t["op"], fg=t["text"],
                            activebackground=t["op_hover"])
            else:
                b.configure(bg=t["btn"], fg=t["text"],
                            activebackground=t["btn_hover"])
            b.grid_configure(padx=sp, pady=sp)
        if self.second:
            self.second_btn.configure(bg=t["equals"], fg=t["equals_text"])
        self.deg_btn.configure(text="DEG" if self.degrees else "RAD")
        self._apply_mode()
        if save:
            save_settings(self.settings)

    def _cycle_theme(self):
        keys = list(THEMES.keys())
        i = keys.index(self.settings["theme_name"]) \
            if self.settings["theme_name"] in keys else 0
        self.settings["theme_name"] = keys[(i + 1) % len(keys)]
        self.settings["custom_colors"] = {}
        self._apply_all()

    # ---------------- Fenetre Personnaliser ----------------
    def _open_settings(self):
        s = self.settings
        win = tk.Toplevel(self)
        win.title("Personnaliser la calculatrice")
        win.geometry("520x560")
        win.transient(self)
        win.grab_set()
        nb = tk.Frame(win)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        # --- Bloc Theme + couleurs ---
        tk.Label(nb, text="Theme pret a l'emploi :",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        theme_var = tk.StringVar(value=s["theme_name"])
        # Swatches des couleurs libres, remplis plus bas ; references
        # gardees pour pouvoir les rafraichir quand le theme change.
        self._color_swatches = {}
        def _on_theme_change():
            # CORRECTIF : appliquer le theme IMMEDIATEMENT au clic,
            # sans attendre le bouton Fermer. On efface aussi les
            # couleurs libres, sinon elles masquent le nouveau theme
            # (c'etait le bug : Violet coche mais Bleu nuit visible).
            s["theme_name"] = theme_var.get()
            s["custom_colors"] = {}
            self._apply_all()
            # Rafraichir les pastilles de couleurs libres
            new_cur = self._colors()
            for _k, _sw in getattr(self, "_color_swatches", {}).items():
                try:
                    _sw.configure(bg=new_cur.get(_k, "#888888"))
                except Exception:
                    pass
        tf = tk.Frame(nb)
        tf.pack(fill="x", pady=4)
        for k, lab in THEME_LABELS.items():
            tk.Radiobutton(tf, text=lab, variable=theme_var, value=k,
                           font=("Segoe UI", 10),
                           command=_on_theme_change).pack(anchor="w")
        tk.Label(nb, text="Couleurs libres (remplacent le theme) :",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 2))
        self._color_vars = {}
        cf = tk.Frame(nb)
        cf.pack(fill="x")
        cur = self._colors()
        for row, (key, lab) in enumerate(COLOR_LABELS.items()):
            tk.Label(cf, text=lab, font=("Segoe UI", 10)).grid(
                row=row, column=0, sticky="w", pady=2)
            sw = tk.Label(cf, text="   ", bg=cur.get(key, "#888888"),
                          relief="solid", bd=1)
            sw.grid(row=row, column=1, padx=8)
            self._color_swatches[key] = sw
            def pick(k=key, swatch=sw):
                # Couleur de depart = couleur ACTUELLE (pas celle
                # figee a l'ouverture de la fenetre)
                fresh = self._colors()
                c = colorchooser.askcolor(color=fresh.get(k),
                                          title=COLOR_LABELS[k])
                if c and c[1]:
                    s.setdefault("custom_colors", {})[k] = c[1]
                    if k == "equals":
                        s["custom_colors"]["accent"] = c[1]
                        s["custom_colors"]["equals_hover"] = c[1]
                    swatch.configure(bg=c[1])
                    # CORRECTIF : application immediate et sauvegarde
                    self._apply_all()
            tk.Button(cf, text="Choisir...", command=pick).grid(
                row=row, column=2, pady=2)
        def _clear_custom():
            s["custom_colors"] = {}
            self._apply_all()
            _new = self._colors()
            for _k, _sw in getattr(self, "_color_swatches", {}).items():
                try:
                    _sw.configure(bg=_new.get(_k, "#888888"))
                except Exception:
                    pass
        tk.Button(nb, text="Effacer les couleurs libres",
                  command=_clear_custom).pack(anchor="w", pady=6)
        # --- Bloc Police / tailles / style ---
        tk.Label(nb, text="Police, tailles et style :",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(8, 2))
        font_var = tk.StringVar(value=s["font_family"])
        tk.OptionMenu(nb, font_var, "Segoe UI", "Arial", "Verdana",
                      "Consolas", "Tahoma",
                      command=lambda _v: (s.update(
                          font_family=font_var.get()),
                          self._apply_all())
                      ).pack(anchor="w", fill="x")
        def slider(label, key, lo, hi):
            tk.Label(nb, text=label, font=("Segoe UI", 10)).pack(anchor="w")
            v = tk.Scale(nb, from_=lo, to=hi, orient="horizontal",
                         command=lambda val, k=key: (
                             s.update({k: int(float(val))}),
                             self._apply_all()))
            v.set(s[key])
            v.pack(fill="x")
            return v
        slider("Taille du gros chiffre affiche", "display_size", 20, 48)
        slider("Taille du texte des boutons", "button_size", 10, 20)
        slider("Espacement entre les boutons", "spacing", 0, 6)
        style_var = tk.StringVar(value=s["button_style"])
        tk.Label(nb, text="Style des boutons :", font=("Segoe UI", 10)
                 ).pack(anchor="w")
        for val, lab in (("plat", "Plat (moderne)"),
                         ("relief", "Relief leger"), ("bordure", "Bordure")):
            tk.Radiobutton(nb, text=lab, variable=style_var, value=val,
                command=lambda: (s.update(button_style=style_var.get()),
                                 self._apply_all())).pack(anchor="w")
        win._vars = (theme_var, font_var, style_var)
        # Bouton page 2
        tk.Button(win, text="Plus de reglages (fenetre, affichage...) ->",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: self._open_settings2(win, theme_var,
                                                       font_var)
                  ).pack(pady=6)
        tk.Button(win, text="Fermer", command=lambda: (
            s.update(theme_name=theme_var.get(),
                     font_family=font_var.get()), self._apply_all(),
            win.destroy())).pack(pady=2)

    def _open_settings2(self, parent_win, theme_var, font_var):
        s = self.settings
        parent_win.destroy()
        win = tk.Toplevel(self)
        win.title("Personnaliser - suite")
        win.geometry("520x600")
        win.transient(self)
        win.grab_set()
        nb = tk.Frame(win)
        nb.pack(fill="both", expand=True, padx=12, pady=10)
        tk.Label(nb, text="Fenetre :", font=("Segoe UI", 11, "bold")
                 ).pack(anchor="w")
        size_var = tk.StringVar(value=s["window_size"])
        for val, lab in (("petite", "Petite"), ("moyenne", "Moyenne"),
                         ("grande", "Grande"), ("tres_grande", "Tres grande")):
            tk.Radiobutton(nb, text=lab, variable=size_var, value=val,
                command=lambda: (s.update(window_size=size_var.get()),
                                 self._apply_all())).pack(anchor="w")
        top_var = tk.BooleanVar(value=bool(s["always_on_top"]))
        tk.Checkbutton(nb, text="Toujours au premier plan",
            variable=top_var, font=("Segoe UI", 10),
            command=lambda: (s.update(always_on_top=top_var.get()),
                             self._apply_all())).pack(anchor="w", pady=2)
        tk.Label(nb, text="Transparence de la fenetre :",
                 font=("Segoe UI", 10)).pack(anchor="w")
        op = tk.Scale(nb, from_=0.5, to=1.0, resolution=0.05,
                      orient="horizontal",
                      command=lambda v: (s.update(opacity=float(v)),
                                         self._apply_all()))
        op.set(s["opacity"])
        op.pack(fill="x")
        tk.Label(nb, text="Affichage et calcul :",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 2))
        hist_var = tk.BooleanVar(value=bool(s["show_history"]))
        tk.Checkbutton(nb, text="Montrer l'historique a droite",
            variable=hist_var, font=("Segoe UI", 10),
            command=lambda: (s.update(show_history=hist_var.get()),
                             self._apply_all())).pack(anchor="w")
        keep_var = tk.BooleanVar(value=bool(s["keep_history"]))
        tk.Checkbutton(nb, text="Garder l'historique entre les sessions",
            variable=keep_var, font=("Segoe UI", 10),
            command=lambda: s.update(keep_history=keep_var.get())
            ).pack(anchor="w")
        thou_var = tk.BooleanVar(value=bool(s["thousands_sep"]))
        tk.Checkbutton(nb, text="Separateur de milliers (ex. 1 234,5)",
            variable=thou_var, font=("Segoe UI", 10),
            command=lambda: (s.update(thousands_sep=thou_var.get()),
                             self._refresh())).pack(anchor="w")
        tk.Label(nb, text="Nombre max. de decimales affichees :",
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(6, 0))
        dec = tk.Scale(nb, from_=2, to=15, orient="horizontal",
                       command=lambda v: s.update(decimals=int(float(v))))
        dec.set(s["decimals"])
        dec.pack(fill="x")
        sep_var = tk.StringVar(value=s["decimal_sep"])
        tk.Label(nb, text="Separateur decimal :", font=("Segoe UI", 10)
                 ).pack(anchor="w")
        for val, lab in ((",", "Virgule  (1,5)"), (".", "Point  (1.5)")):
            tk.Radiobutton(nb, text=lab, variable=sep_var, value=val,
                command=lambda: s.update(decimal_sep=sep_var.get())
                ).pack(anchor="w")
        deg_var = tk.BooleanVar(value=bool(s["default_degrees"]))
        tk.Checkbutton(nb, text="Demarrer en DEG (sinon RAD)",
            variable=deg_var, font=("Segoe UI", 10),
            command=lambda: s.update(default_degrees=deg_var.get())
            ).pack(anchor="w", pady=4)
        tk.Button(nb, text="REINITIALISER TOUT (comme au debut)",
                  fg="#b00020", font=("Segoe UI", 10, "bold"),
                  command=lambda: self._reset_all(win)).pack(pady=12)
        tk.Button(nb, text="Enregistrer et fermer",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: (s.update(theme_name=theme_var.get(),
                    font_family=font_var.get()), self._apply_all(),
                    win.destroy())).pack()

    def _reset_all(self, win=None):
        if messagebox.askyesno("Reinitialiser",
                               "Tout remettre comme au debut ?"):
            self.settings = dict(DEFAULT_SETTINGS)
            self.degrees = True
            self.mode = "scientifique"
            if win:
                win.destroy()
            self._apply_all()

    # ---------------- Calcul (inchange, sauf formatage) ----------------
    def _refresh(self):
        txt = self.expression if self.expression else "0"
        if self.settings.get("thousands_sep") and txt.replace(",", "").replace(".", "").replace("−", "").replace("-", "").isdigit():
            sep = self.settings.get("decimal_sep", ",")
            raw = txt.replace(",", ".")
            try:
                val = float(raw)
                txt = self._format(val)
            except Exception:
                pass
        elif self.settings.get("decimal_sep") == ".":
            txt = txt.replace(",", ".")
        self.display.configure(text=txt)

    def _insert(self, text):
        if self.mode == "normal" and text in ("π", "e", "^"):
            return
        if self.just_evaluated and text not in "+−×÷^%":
            self.expression = ""
        # Toute nouvelle saisie annule la repetition du =
        # (elle sera recalculee au prochain =)
        if self.just_evaluated:
            self.last_op = None
            self.last_operand = None
        self.just_evaluated = False
        if (text in ("π", "e", "(") and self.expression
                and (self.expression[-1].isdigit()
                     or self.expression[-1] in ")πe")):
            self.expression += "×"
        self.expression += text
        self._refresh()

    def _func(self, name):
        if self.second:
            name = {"sin": "asin", "cos": "acos", "tan": "atan",
                    "ln": "exp", "log": "pow10"}.get(name, name)
        if self.expression and (self.expression[-1].isdigit()
                                or self.expression[-1] in ")πe"):
            self.expression += "×"
        if name == "exp":
            self._insert("e^(")
        elif name == "pow10":
            self._insert("10^(")
        else:
            self._insert(name + "(")

    def _clear(self):
        self.expression = ""
        self.just_evaluated = False
        self.last_op = None
        self.last_operand = None
        self.expr_label.configure(text="")
        self._refresh()

    def _backspace(self):
        self.expression = self.expression[:-1]
        self.just_evaluated = False
        self.last_op = None
        self.last_operand = None
        self._refresh()

    def _evaluate(self, expr):
        s = (expr.replace("×", "*").replace("÷", "/")
                 .replace("−", "-").replace(",", ".")
                 .replace("π", " pi ").replace("^", "**"))
        s = re.sub(r"([\d)])\s*(\(|pi\b|sin\b|cos\b|tan\b|asin\b|acos\b"
                   r"|atan\b|ln\b|log\b|sqrt\b)", r"\1*\2", s)
        s = re.sub(r"(pi\b|\))\s*(\d)", r"\1*\2", s)
        s += ")" * max(0, s.count("(") - s.count(")"))
        if self.degrees:
            sin = lambda x: math.sin(math.radians(x))  # noqa: E731
            cos = lambda x: math.cos(math.radians(x))  # noqa: E731
            tan = lambda x: math.tan(math.radians(x))  # noqa: E731
            asin = lambda x: math.degrees(math.asin(x))  # noqa: E731
            acos = lambda x: math.degrees(math.acos(x))  # noqa: E731
            atan = lambda x: math.degrees(math.atan(x))  # noqa: E731
        else:
            sin, cos, tan = math.sin, math.cos, math.tan
            asin, acos, atan = math.asin, math.acos, math.atan
        env = {"sin": sin, "cos": cos, "tan": tan, "asin": asin,
               "acos": acos, "atan": atan, "ln": math.log,
               "log": math.log10, "sqrt": math.sqrt, "exp": math.exp,
               "abs": abs, "pi": math.pi, "e": math.e}
        result = eval(s, {"__builtins__": {}}, env)  # noqa: S307
        if isinstance(result, complex):
            raise ValueError("Resultat complexe")
        return float(result)

    def _format(self, value):
        dec = int(self.settings.get("decimals", 10))
        sep = self.settings.get("decimal_sep", ",")
        if value == int(value) and abs(value) < 1e16:
            txt = str(int(value))
        else:
            txt = f"{value:.{dec}g}"
        if self.settings.get("thousands_sep") and "e" not in txt.lower():
            parts = txt.split(".")
            ip = parts[0].lstrip("-")
            sign = "-" if parts[0].startswith("-") else ""
            grouped = ""
            while len(ip) > 3:
                grouped = " " + ip[-3:] + grouped
                ip = ip[:-3]
            txt = sign + ip + grouped + (("." + parts[1]) if len(parts) > 1 else "")
        return txt.replace(".", sep) if sep == "," else txt

    def _extract_last_operation(self, expr):
        """Trouve la derniere operation binaire de haut niveau.

        Retourne (operateur, operande_droite) ou None.
        Ex. : '9+9' -> ('+', '9') ; '2+3×4' -> ('×', '4') ;
        '(2+3)×4' -> ('×', '4') ; 'sin(30)' -> None.
        Les operateurs entre parentheses sont ignores, et un
        signe au debut ou apres '(' / un operateur est unaire.
        """
        depth = 0
        last_idx = -1
        last_char = None
        for i, c in enumerate(expr):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif depth == 0 and c in "+−×÷-*/":
                if i > 0 and (expr[i - 1].isdigit()
                              or expr[i - 1] in ")πe%,"):
                    if i + 1 < len(expr):
                        last_idx = i
                        last_char = c
        if last_idx < 0:
            return None
        operand = expr[last_idx + 1:].strip()
        if not operand:
            return None
        return (last_char, operand)

    def _equals(self):
        if not self.expression:
            return
        # Repetition : on vient d'appuyer sur = et on rappuie dessus
        is_repeat = bool(self.just_evaluated
                         and self.last_op is not None
                         and self.last_operand is not None)
        if self.just_evaluated and not is_repeat:
            # = sur un simple resultat, sans operation a repeter :
            # ne pas ajouter '18 = 18' en boucle dans l'historique.
            return
        if is_repeat:
            shown = (f"{self.expression}{self.last_op}"
                     f"{self.last_operand}")
        else:
            shown = self.expression
        try:
            value = self._evaluate(shown)
            text = self._format(value)
        except Exception:
            self.expr_label.configure(text=shown)
            self.display.configure(text="Erreur")
            self.expression = ""
            self.just_evaluated = True
            self.last_op = None
            self.last_operand = None
            return
        if not is_repeat:
            found = self._extract_last_operation(shown)
            if found:
                self.last_op, self.last_operand = found
            else:
                self.last_op = None
                self.last_operand = None
        self.expr_label.configure(text=shown + " =")
        self.expression = text
        self.just_evaluated = True
        self._refresh()
        entry = f"{shown} = {text}"
        self.hist_items.append(entry)
        self.history.insert("end", entry)
        if self.settings.get("keep_history"):
            self.settings["saved_history"] = self.hist_items[-100:]
            save_settings(self.settings)

    def _current_value(self):
        return 0.0 if not self.expression else self._evaluate(self.expression)

    def _unary(self, op):
        try:
            v = self._current_value()
            if op == "sqrt":
                v = math.sqrt(v)
            elif op == "square":
                v = v * v
            elif op == "inv":
                v = 1 / v
            elif op == "abs":
                v = abs(v)
        except Exception:
            self.display.configure(text="Erreur")
            self.expression = ""
            return
        self.expression = self._format(v)
        self.just_evaluated = True
        self.last_op = None
        self.last_operand = None
        self._refresh()

    def _factorial(self):
        try:
            v = self._current_value()
            if v < 0 or v != int(v):
                raise ValueError
            v = float(math.factorial(int(v)))
        except Exception:
            self.display.configure(text="Erreur")
            self.expression = ""
            return
        self.expression = self._format(v)
        self.just_evaluated = True
        self.last_op = None
        self.last_operand = None
        self._refresh()

    def _negate(self):
        if self.expression:
            if self.expression.startswith(("−", "-")):
                self.expression = self.expression[1:]
            else:
                self.expression = "−" + self.expression
            self.last_op = None
            self.last_operand = None
            self._refresh()

    def _toggle_deg(self):
        self.degrees = not self.degrees
        self.deg_btn.configure(text="DEG" if self.degrees else "RAD")
        self.settings["default_degrees"] = self.degrees
        save_settings(self.settings)

    def _toggle_second(self):
        self.second = not self.second
        for btn, normal, alt in (
                (self.btn_sin, "sin", "asin"), (self.btn_cos, "cos", "acos"),
                (self.btn_tan, "tan", "atan"), (self.btn_ln, "ln", "e^x"),
                (self.btn_log, "log", "10^x")):
            btn.configure(text=alt if self.second else normal)
        self._apply_all()

    def _mem_clear(self):
        self.memory = 0.0

    def _mem_store(self):
        try:
            self.memory = self._current_value()
        except Exception:
            pass

    def _mem_recall(self):
        self.expression = self._format(self.memory)
        self.just_evaluated = False
        self.last_op = None
        self.last_operand = None
        self._refresh()

    def _mem_add(self):
        try:
            self.memory += self._current_value()
        except Exception:
            pass

    def _mem_sub(self):
        try:
            self.memory -= self._current_value()
        except Exception:
            pass

    def _history_click(self, _event=None):
        sel = self.history.curselection()
        if not sel:
            return
        self.expression = self.hist_items[sel[0]].rsplit("=", 1)[-1].strip()
        self.just_evaluated = False
        self.last_op = None
        self.last_operand = None
        self._refresh()

    def _clear_history(self):
        self.hist_items.clear()
        self.history.delete(0, "end")
        if self.settings.get("keep_history"):
            self.settings["saved_history"] = []
            save_settings(self.settings)

    def _on_key(self, event):
        ch = event.char
        if ch.isdigit() or ch in ".,":
            self._insert("," if ch in ".," else ch)
        elif ch == "+":
            self._insert("+")
        elif ch == "-":
            self._insert("−")
        elif ch == "*":
            self._insert("×")
        elif ch == "/":
            self._insert("÷")
        elif ch == "%" and self.mode == "scientifique":
            self._insert("%")
        elif ch == "(":
            self._insert("(")
        elif ch == ")":
            self._insert(")")
        elif ch in ("\r", "\n") or event.keysym == "Return":
            self._equals()
        elif event.keysym == "Escape":
            self._clear()
        elif event.keysym == "BackSpace":
            self._backspace()
        elif event.keysym.lower() == "m" and event.state & 0x4:
            self._toggle_mode()  # Ctrl+M : basculer Normal/Scientifique
        else:
            return
        return "break"


if __name__ == "__main__":
    Calculatrice().mainloop()
