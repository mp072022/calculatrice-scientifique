# Calculadora científica

Calculadora científica para Windows, en Python (tkinter). Un solo archivo, no hay que instalar nada más que Python.

[Version française](README.fr.md) · [English version](README.md)

## Ejecutarla

Haz doble clic en `calculatrice-scientifique.py` (se necesita Python 3, tkinter viene incluido con Python).

## Qué hace

- Cálculos básicos, paréntesis, %, separador decimal
- Funciones científicas: sin, cos, tan, log, ln, raíz cuadrada, x², xʸ, 1/x, |x|, factorial (n!), π y e
- Botón **2nd** para las funciones inversas (asin, acos, atan, e^x, 10^x)
- **DEG/RAD** para los ángulos
- Memoria: MC, MR, M+, M−, MS
- Historial de cálculos en el que se puede hacer clic
- Teclado completo: dígitos, + − * /, Enter para =, Esc para borrar

## Modos y personalización

- **Modo Normal / Científico**: botón arriba a la izquierda, o Ctrl+M
- **Personalizar**: 8 temas listos (Oscuro, Claro, Azul noche, Verde bosque, Violeta, Naranja, Rosa, Negro puro), colores libres, fuente, tamaño de los dígitos y de los botones, tamaño de la ventana, transparencia, número de decimales, coma o punto, separador de miles
- **Idioma**: English (predeterminado), Français, Español — en la ventana Personalizar
- Los ajustes se guardan automáticamente en `calculatrice_config.json`

## Crear un .exe

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name "Calculatrice-scientifique" calculatrice-scientifique.py
```

El archivo `.exe` queda en la carpeta `dist`.
