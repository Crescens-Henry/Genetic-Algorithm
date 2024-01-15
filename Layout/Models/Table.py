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
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    return tree


def llenar_tabla(poblacion, tabla):
    for i, individuo in enumerate(poblacion):
        # Convierte el número 'i' del individuo a binario y quita el prefijo '0b'
        individuo_binario = bin(individuo.i)[2:].zfill(5)

        # Format the 'individuo.x' value as a floating-point number with 2 decimal places
        individuo_x = "{:.2f}".format(individuo.x)

        # Inserta una nueva fila en la tabla
        tabla.insert("", "end", values=(
            i + 1, individuo_binario, individuo.i, individuo_x, individuo.fx))
