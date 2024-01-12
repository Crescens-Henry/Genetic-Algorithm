import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


def section(parent, title):
    frame = ttk.Frame(parent, padding=(10, 0, 10, 0))
    frame.grid(sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
    frame.columnconfigure(1, weight=1)
    ttk.Label(frame, text=title, font=('Helvetica', 12, 'bold')).grid(column=0, row=0, sticky=(tk.W, tk.E), padx=(0, 5),
                                                                      pady=(0, 5))
    return frame


def set_widget_width(widget, width):
    widget.config(width=width)


def update_graph(x_values, y_values1, y_values2, y_values3, ax):
    ax.clear()
    ax.plot(x_values, y_values1, label='Data 1')
    ax.plot(x_values, y_values2, label='Data 2')
    ax.plot(x_values, y_values3, label='Data 3')
    ax.legend()
    ax.set_title('Fluctuación de Datos en Tiempo Real')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Valor')


def generate_random_data():
    return random.random() * 10


def update_data(x_values, y_values1, y_values2, y_values3):
    x_values.append(len(x_values))
    y_values1.append(generate_random_data())
    y_values2.append(generate_random_data())
    y_values3.append(generate_random_data())


def Interface():
    root = tk.Tk()
    root.title("Algoritmos Genéticos By Crescens")

    entry_width = 8

    frame_poblacion = section(root, "Tamaño de la Población")
    ttk.Label(frame_poblacion, text="Tamaño Inicial:").grid(column=0, row=1, sticky=tk.W, pady=1)
    initial_population = ttk.Entry(frame_poblacion, width=entry_width)
    initial_population.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(initial_population, entry_width)

    ttk.Label(frame_poblacion, text="Tamaño Máximo:").grid(column=0, row=2, sticky=tk.W, pady=1)
    limit_population = ttk.Entry(frame_poblacion, width=entry_width)
    limit_population.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(limit_population, entry_width)

    frame_mutacion = section(root, "Probabilidades de Mutación")
    ttk.Label(frame_mutacion, text="Por Individuo:").grid(column=0, row=1, sticky=tk.W, pady=1)
    individual_mutation = ttk.Entry(frame_mutacion, width=entry_width)
    individual_mutation.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(individual_mutation, entry_width)

    ttk.Label(frame_mutacion, text="Por Gen:").grid(column=0, row=2, sticky=tk.W, pady=1)
    gene_mutation = ttk.Entry(frame_mutacion, width=entry_width)
    gene_mutation.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(gene_mutation, entry_width)

    frame_rango = section(root, "Rango de Posible Solución")
    ttk.Label(frame_rango, text="Rango minimo de X:").grid(column=0, row=1, sticky=tk.W, pady=1)
    minimum_range_of_x = ttk.Entry(frame_rango, width=entry_width)
    minimum_range_of_x.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)

    ttk.Label(frame_rango, text="Rango maximo de X:").grid(column=2, row=1, sticky=tk.W, pady=1)
    maximum_range_of_x = ttk.Entry(frame_rango, width=entry_width)
    maximum_range_of_x.grid(column=3, row=1, sticky=(tk.W, tk.E), pady=1)

    ttk.Label(frame_rango, text="Rango minimo de Y:").grid(column=0, row=2, sticky=tk.W, pady=1)
    minimum_range_of_y = ttk.Entry(frame_rango, width=entry_width)
    minimum_range_of_y.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)

    ttk.Label(frame_rango, text="Rango maximo de Y:").grid(column=2, row=2, sticky=tk.W, pady=1)
    maximum_range_of_y = ttk.Entry(frame_rango, width=entry_width)
    maximum_range_of_y.grid(column=3, row=2, sticky=(tk.W, tk.E), pady=1)

    frame_cruza = section(root, "Probabilidad de Cruza")
    ttk.Label(frame_cruza, text="Probabilidad de Cruza:").grid(column=0, row=1, sticky=tk.W, pady=1)
    entry_prob_cruza = ttk.Entry(frame_cruza, width=entry_width)
    entry_prob_cruza.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(entry_prob_cruza, entry_width)

    frame_table = ttk.Frame(root, padding=10)
    frame_table.grid(row=5, column=0, columnspan=2, pady=10)
    tree = ttk.Treeview(frame_table, columns=("ID", "Individuo", "i", "X", "f(x)"), show="headings")
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
    frame_table.columnconfigure(0, weight=1)
    frame_table.rowconfigure(0, weight=1)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=5, rowspan=6, pady=10)

    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []

    def update():
        update_data(x_values, y_values1, y_values2, y_values3)
        update_graph(x_values, y_values1, y_values2, y_values3, ax)
        canvas.draw()
        root.after(1000, update)

    update()

    root.mainloop()
