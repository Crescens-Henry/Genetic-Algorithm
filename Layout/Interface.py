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
    equation.insert(0, "sin(x) + cos(x)")
    equation.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    
    ttk.Label(frame_init, text="Valor minimo para X:").grid(
        column=0, row=2, sticky=tk.W, pady=1)
    min_result_entry = ttk.Entry(frame_init, width=entry_width)
    min_result_entry.insert(0, "3")
    min_result_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    
    ttk.Label(frame_init, text="Valor máximo para X:").grid(
        column=0, row=3, sticky=tk.W, pady=1)
    max_result_entry = ttk.Entry(frame_init, width=entry_width)
    max_result_entry.insert(0, "7")
    max_result_entry.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=1)

    ttk.Label(frame_init, text="Delta:").grid(
        column=0, row=5, sticky=tk.W, pady=1)
    delta_deseada = ttk.Entry(frame_init, width=entry_width)
    delta_deseada.insert(0, "0.05")
    delta_deseada.grid(column=1, row=5, sticky=(tk.W, tk.E), pady=1)
    
    ttk.Label(frame_init, text="Generaciones:").grid(
        column=0, row=4, sticky=tk.W, pady=1)
    iteraciones = ttk.Entry(frame_init, width=entry_width)
    iteraciones.insert(0, "4")
    iteraciones.grid(column=1, row=4, sticky=(tk.W, tk.E), pady=1)


    frame_poblacion = section(root, "Tamaño de la Población")
    ttk.Label(frame_poblacion, text="Tamaño Inicial:").grid(
        column=0, row=1, sticky=tk.W, pady=1)
    initial_population = ttk.Entry(frame_poblacion, width=entry_width)
    initial_population.insert(0, "3")
    initial_population.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(initial_population, entry_width)

    ttk.Label(frame_poblacion, text="Tamaño Máximo:").grid(
        column=0, row=2, sticky=tk.W, pady=1)
    limit_population = ttk.Entry(frame_poblacion, width=entry_width)
    limit_population.insert(0, "7")
    limit_population.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(limit_population, entry_width)

    frame_mutacion = section(root, "Probabilidades de Mutación")
    ttk.Label(frame_mutacion, text="Por Individuo:").grid(
        column=0, row=1, sticky=tk.W, pady=1)
    individual_mutation = ttk.Entry(frame_mutacion, width=entry_width)
    individual_mutation.insert(0, "0.9")
    individual_mutation.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(individual_mutation, entry_width)

    ttk.Label(frame_mutacion, text="Por Gen:").grid(
        column=0, row=2, sticky=tk.W, pady=1)
    gene_mutation = ttk.Entry(frame_mutacion, width=entry_width)
    gene_mutation.insert(0, "0.9")
    gene_mutation.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(gene_mutation, entry_width)

    frame_cruza = section(root, "Probabilidad de Cruza")
    
    ttk.Label(frame_cruza, text="Porcentaje de cruce:").grid(
        column=0, row=2, sticky=tk.W, pady=1)
    porcentaje_cruza = ttk.Entry(frame_cruza, width=entry_width)
    porcentaje_cruza.insert(0, "0.9")
    porcentaje_cruza.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=1)
    set_widget_width(porcentaje_cruza, entry_width)

    frame_table = ttk.Frame(root, padding=10)
    frame_table.grid(row=5, column=0, columnspan=2, pady=10)
    tree = create_table(frame_table)

    
    
    def minimizar():
        AlgoritmoGenetico.poblacion_final = []
        tree.delete(*tree.get_children())
        maximizar = False
            
        equation_value = equation.get()
        
        minimo = int(min_result_entry.get())
        maximo = int(max_result_entry.get())
        delta_deseada_value = float(delta_deseada.get())
        
        iteration = int(iteraciones.get())
        
        initial_population_value = int(initial_population.get())
        limit_population_value = int(limit_population.get())
        individual_mutation_value = float(individual_mutation.get())
        gene_mutation_value = float(gene_mutation.get())
        porcentaje_cruza_value = float(porcentaje_cruza.get())
        
        AlgoritmoGenetico(minimo, maximo, delta_deseada_value, equation_value, initial_population_value, limit_population_value, individual_mutation_value, gene_mutation_value, iteration, porcentaje_cruza_value, maximizar,tree)
        

    button = ttk.Button(frame_init, text="Minimizacion",
                        command=minimizar)
    button.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)

    def maximizar():
        # Crear una figura y los ejes
        AlgoritmoGenetico.poblacion_final = []
        tree.delete(*tree.get_children())
        maximizar = True
            
        equation_value = equation.get()
        
        minimo = int(min_result_entry.get())
        maximo = int(max_result_entry.get())
        delta_deseada_value = float(delta_deseada.get())
        
        iteration = int(iteraciones.get())
        
        initial_population_value = int(initial_population.get())
        limit_population_value = int(limit_population.get())
        individual_mutation_value = float(individual_mutation.get())
        gene_mutation_value = float(gene_mutation.get())
        porcentaje_cruza_value = float(porcentaje_cruza.get())
        
        AlgoritmoGenetico(minimo, maximo, delta_deseada_value, equation_value, initial_population_value, limit_population_value, individual_mutation_value, gene_mutation_value, iteration, porcentaje_cruza_value, maximizar,tree)
        


    button = ttk.Button(frame_init, text="Maximizacion",
                        command=maximizar)
    button.grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)

    root.mainloop()
