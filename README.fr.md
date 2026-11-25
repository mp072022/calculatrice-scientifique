# Calculatrice scientifique

Calculatrice scientifique pour Windows, en Python (tkinter). Un seul fichier, rien à installer d'autre que Python.

[English version](README.md) · [Versión en español](README.es.md)

## Lancer

Double-cliquer sur `calculatrice-scientifique.py` (Python 3 requis, tkinter est inclus avec Python).

## Ce qu'elle fait

- Calculs de base, parenthèses, %, virgule décimale
- Fonctions scientifiques : sin, cos, tan, log, ln, racine carrée, x², xʸ, 1/x, |x|, factorielle (n!), π et e
- Bouton **2nd** pour les inverses (asin, acos, atan, e^x, 10^x)
- **DEG/RAD** pour les angles
- Mémoire : MC, MR, M+, M−, MS
- Historique cliquable des calculs
- Clavier complet : chiffres, + − * /, Entrée pour =, Échap pour effacer

## Modes et personnalisation

- **Mode Normal / Scientifique** : bouton en haut à gauche, ou Ctrl+M
- **Personnaliser** : 8 thèmes prêts (Sombre, Clair, Bleu nuit, Vert forêt, Violet, Orange, Rose, Noir pur), couleurs libres, police, taille des chiffres et des boutons, taille de la fenêtre, transparence, nombre de décimales, virgule ou point, séparateur de milliers
- **Langue** : English (par défaut), Français, Español — dans la fenêtre Personnaliser
- Les réglages sont sauvegardés automatiquement dans `calculatrice_config.json`

## En faire un .exe

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name "Calculatrice-scientifique" calculatrice-scientifique.py
```

Le fichier `.exe` se trouve ensuite dans le dossier `dist`.
