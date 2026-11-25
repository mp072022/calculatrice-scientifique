# Scientific Calculator

Scientific calculator for Windows, written in Python (tkinter). A single file, nothing else to install besides Python.

[Version française](README.md) · [Versión en español](README.es.md)

## Run it

Double-click `calculatrice-scientifique.py` (Python 3 required, tkinter comes with Python).

## What it does

- Basic calculations, parentheses, %, decimal separator
- Scientific functions: sin, cos, tan, log, ln, square root, x², xʸ, 1/x, |x|, factorial (n!), π and e
- **2nd** button for inverse functions (asin, acos, atan, e^x, 10^x)
- **DEG/RAD** for angles
- Memory: MC, MR, M+, M−, MS
- Clickable calculation history
- Full keyboard support: digits, + − * /, Enter for =, Esc to clear

## Modes and customization

- **Normal / Scientific mode**: button at the top left, or Ctrl+M
- **Customize**: 8 ready-made themes (Dark, Light, Night blue, Forest green, Purple, Orange, Pink, Pure black), free colors, font, digit and button sizes, window size, transparency, number of decimals, comma or dot separator, thousands separator
- Settings are saved automatically in `calculatrice_config.json`

## Build a .exe

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name "Calculatrice-scientifique" calculatrice-scientifique.py
```

The `.exe` file is then in the `dist` folder.
