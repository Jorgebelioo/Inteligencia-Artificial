# main.py
import tkinter as tk
from interfaz import InterfazExperto

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazExperto(root)
    root.mainloop()
