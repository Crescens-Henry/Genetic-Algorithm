import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from Layout.Models.Table import create_table
from Layout.UIUtils import section, set_widget_width
from GeneticAlgorithm.AlgorithmPrincipal import AlgoritmoGenetico, Individuo

def Interface():
    root = tk.Tk()
    root.title("Algoritmos Genéticos By Crescens")

    entry_width = 8

    frame_init = section(root, "Ecuacion principal:")
    ttk.Label(frame_init, text="f(x):").grid(
        column=0, row=1, sticky=tk.W, padx=5, pady=5)
    equation = ttk.Entry(frame_init, width=entry_width)
    equation.insert(0, "x**3-x**3*cos(5*x)")
    equation.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    
    ttk.Label(frame_init, text="Valor máximo para X:").grid(
        column=0, row=2, sticky=tk.W, pady=1)
    max_result_entry = ttk.Entry(frame_init, width=entry_width)
    max_result_entry.insert(0, "20")
    max_result_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)

    ttk.Label(frame_init, text="Valor minimo para X:").grid(
        column=0, row=3, sticky=tk.W, pady=1)
    min_result_entry = ttk.Entry(frame_init, width=entry_width)
    min_result_entry.insert(0, "2")
    min_result_entry.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=1)
    
    ttk.Label(frame_init, text="Iteraciones:").grid(
        column=0, row=4, sticky=tk.W, pady=1)
    iteraciones = ttk.Entry(frame_init, width=entry_width)
    iteraciones.insert(0, "100")
    iteraciones.grid(column=1, row=4, sticky=(tk.W, tk.E), pady=1)

    frame_poblacion = section(root, "Tamaño de la Población")
    ttk.Label(frame_poblacion, text="Tamaño Inicial:").grid(
        column=0, row=1, sticky=tk.W, pady=1)
    initial_population = ttk.Entry(frame_poblacion, width=entry_width)
    initial_population.insert(0, "12")
    initial_population.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(initial_population, entry_width)

    ttk.Label(frame_poblacion, text="Tamaño Máximo:").grid(
        column=0, row=2, sticky=tk.W, pady=1)
    limit_population = ttk.Entry(frame_poblacion, width=entry_width)
    limit_population.insert(0, "20")
    limit_population.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(limit_population, entry_width)

    frame_mutacion = section(root, "Probabilidades de Mutación")
    ttk.Label(frame_mutacion, text="Por Individuo:").grid(
        column=0, row=1, sticky=tk.W, pady=1)
    individual_mutation = ttk.Entry(frame_mutacion, width=entry_width)
    individual_mutation.insert(0, "0.65")
    individual_mutation.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(individual_mutation, entry_width)

    ttk.Label(frame_mutacion, text="Por Gen:").grid(
        column=0, row=2, sticky=tk.W, pady=1)
    gene_mutation = ttk.Entry(frame_mutacion, width=entry_width)
    gene_mutation.insert(0, "0.45")
    gene_mutation.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(gene_mutation, entry_width)

    frame_cruza = section(root, "Probabilidad de Cruza")
    ttk.Label(frame_cruza, text="Probabilidad de Cruza:").grid(
        column=0, row=1, sticky=tk.W, pady=1)
    entry_prob_cruza = ttk.Entry(frame_cruza, width=entry_width)
    entry_prob_cruza.insert(0, "0.85")
    entry_prob_cruza.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(entry_prob_cruza, entry_width)

    frame_table = ttk.Frame(root, padding=10)
    frame_table.grid(row=5, column=0, columnspan=2, pady=10)
    tree = create_table(frame_table)

    def handle_minimize_button_click():
        tree.delete(*tree.get_children())
        equation_value = equation.get()
        print(equation_value)
        
        min_result = int(min_result_entry.get())
        max_result = int(max_result_entry.get())
        
        iteration = int(iteraciones.get())
        
        initial_population_value = int(initial_population.get())
        entry_prob_cruza_value = float(entry_prob_cruza.get())
        limit_population_value = int(limit_population.get())
        individual_mutation_value = float(individual_mutation.get())
        gene_mutation_value = float(gene_mutation.get())
        
        minimo, maximo = Individuo.obtener_minimo_maximo(equation_value, min_result, max_result)
        
        algoritmo = AlgoritmoGenetico(initial_population_value, min_result, max_result, minimo, maximo, 5, equation_value)
        algoritmo.ejecutar(iteration, equation_value, min_result, max_result, initial_population_value, entry_prob_cruza_value, limit_population_value, individual_mutation_value, gene_mutation_value, tree)
                

    button = ttk.Button(frame_init, text="Minimizacion",
                        command=handle_minimize_button_click)
    button.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)

    def handle_maximize_button_click():
        pass

    button = ttk.Button(frame_init, text="Maximizacion",
                        command=handle_maximize_button_click)
    button.grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)

    root.mainloop()
