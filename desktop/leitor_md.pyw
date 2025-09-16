#!/usr/bin/env python3
"""
Leitor MD - Launcher Script
This script can be used as the default program for .md files
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from markdown_reader import main
    main()
except ImportError as e:
    # Fallback error dialog
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Erro - Leitor MD",
        f"Erro ao importar dependências:\n{str(e)}\n\n"
        "Certifique-se de que todas as dependências estão instaladas:\n"
        "pip install -r requirements.txt"
    )
    sys.exit(1)
