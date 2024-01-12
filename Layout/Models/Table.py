import tkinter as tk
from tkinter import ttk

def create_table(frame):
    tree = ttk.Treeview(frame, columns=("ID", "Individuo", "i", "X", "f(x)"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Individuo", text="Individuo")
    tree.heading("i", text="i")
    tree.heading("X", text="X")
    tree.heading("f(x)", text="f(x)")
    tree.column("ID", anchor="center", width=90)
    tree.column("Individuo", anchor="center", width=90)
    tree.column("i", anchor="center", width=90)
    tree.column("X", anchor="center", width=90)
    tree.column("f(x)", anchor="center", width=90)
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    return tree

def update_table(tree, x_values, y_values1, y_values2, y_values3):
    values = list(zip(x_values, y_values1, y_values2, y_values3))
    for i in tree.get_children():
        tree.delete(i)
    for i, (x, y1, y2, y3) in enumerate(values, start=1):
        tree.insert("", "end", values=(i, f"Individuo {i}", f"i {i}", f"X {i}", f"f(x) {i}"))
