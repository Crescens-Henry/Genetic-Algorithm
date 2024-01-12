import tkinter as tk
from tkinter import ttk

def section(parent, title):
    frame = ttk.Frame(parent, padding=(10, 0, 10, 0))
    frame.grid(sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
    frame.columnconfigure(1, weight=1)
    ttk.Label(frame, text=title, font=('Helvetica', 12, 'bold')).grid(column=0, row=0, sticky=(tk.W, tk.E), padx=(0, 5),
                                                                      pady=(0, 5))
    return frame

def set_widget_width(widget, width):
    widget.config(width=width)
