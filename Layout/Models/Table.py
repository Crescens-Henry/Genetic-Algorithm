import re
import tkinter as tk
from tkinter import ttk


def create_table(frame):
    tree = ttk.Treeview(frame, columns=("ID", "Individuo",
                        "i", "X", "f(x)"), show="headings")
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
    tree.tag_configure('poblacion_inicial', background='#B5FFB0')
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    return tree

def insertar_datos(tree, individuos, es_poblacion_inicial=True):
    for i, individuo in enumerate(individuos):
        if es_poblacion_inicial:
            tree.insert('', 'end', values=(i+1, str(individuo.individuo), individuo.i, individuo.x, individuo.fx), tags=('poblacion_inicial'))
        else:
            tree.insert('', 'end', values=(i+1, str(individuo.individuo), individuo.i, individuo.x, individuo.fx))