import math
import os
import random
from tkinter import Tk
from matplotlib import pyplot as plt
from sympy import cos, sin, symbols, rad, sympify
import sympy as sp
from Layout.Models import Graphics
from Layout.Models.Table import insertar_datos
import random


class Individuo:
    id_counter = 1
    def __init__(self, individuo, minimo, maximo, delta_deseada, ecuacion):
        self.id = Individuo.id_counter
        Individuo.id_counter += 1
        self.individuo = individuo  
        self.i = int(''.join(map(str, individuo)), 2)
        self.x = self.calcular_x(minimo, maximo, delta_deseada)
        self.fx = self.calcular_fx(ecuacion)
        
    def __str__(self):
        return str(self.individuo)
    
    def __repr__(self):
        return f'Individuo(individuo binario={self.individuo}, decimal={self.i})'

    def calcular_bits (self, minimo, maximo, delta_deseada):
        rango = maximo-minimo
        saltos = (rango/delta_deseada)+1
        bits = math.ceil(math.log2(saltos))
        return bits
    
    def calcular_x(self, minimo, maximo, delta_deseada):
        bits = self.calcular_bits(minimo, maximo, delta_deseada)
        rango = maximo - minimo
        delta = rango / (2 ** bits - 1)
        
        if delta > delta_deseada:
            delta = delta_deseada
        elif delta < delta_deseada:
            delta = delta
        x = minimo + self.i * delta
        
        return x

    def calcular_fx(self, ecuacion):
        try:
            var = sp.symbols('x')
            x_value = self.x
            resultado = sympify(ecuacion).subs(var, x_value)
            resultado = resultado.evalf()
            return resultado
        except Exception as e:
            print("Error al calcular fx:", e)
            return None

class AlgoritmoGenetico:
        def __init__(self, minimo, maximo, delta_deseada,ecuacion,initial_population, limit_population, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar,tree):
            self.poblacion_final = []
            self.ejecutar_algoritmo(minimo, maximo, delta_deseada, ecuacion, initial_population, limit_population, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar,tree)
        
        def inicializar_populacion(self, minimo, maximo, delta_deseada, ecuacion, initial_population):
            poblacion = []
            for _ in range(initial_population):
                # Generar un número binario aleatorio de longitud n
                bits = Individuo.calcular_bits(self, minimo, maximo, delta_deseada)
                individuo_binario = [random.randint(0, 1) for _ in range(bits)]
                
                individuo = Individuo(individuo_binario, minimo, maximo, delta_deseada, ecuacion)

                poblacion.append(individuo)
            return poblacion
        
        def seleccionar_mejores(self, poblacion, porcentaje_cruce, maximizar):

            poblacion = [x for x in poblacion if not isinstance(x, list)]
            if maximizar:
                poblacion_ordenada = sorted(poblacion, key=lambda x: x.fx, reverse=True)
            else:
                poblacion_ordenada = sorted(poblacion, key=lambda x: x.fx)

            num_seleccionados = int(len(poblacion) * porcentaje_cruce)
            mejores_individuos = poblacion_ordenada[:num_seleccionados]
            parejas = []
            parejas_formadas = set()

            # Para cada uno de los individuos en la lista de mejores individuos
            for i in range(0, len(mejores_individuos), 2):
                # Si hay un individuo siguiente para formar una pareja
                if i+1 < len(mejores_individuos):
                    # Forma una pareja con el individuo actual y el siguiente
                    pareja = (mejores_individuos[i].i, mejores_individuos[i+1].i)
                    # Verifica que la pareja no se haya formado antes
                    if pareja not in parejas_formadas:
                        parejas_formadas.add(pareja)
                        parejas.append((mejores_individuos[i], mejores_individuos[i+1]))

            return parejas
        
        def cruzar(self, parejas):
            descendientes = []
            for pareja in parejas:
                individuo1, individuo2 = pareja
                longitud_minima = min(len(individuo1.individuo), len(individuo2.individuo))
                puntos_cruza = random.randint(1, longitud_minima)  # Random number of crossover points
                posiciones_cruza = random.sample(range(1, longitud_minima), min(puntos_cruza, longitud_minima - 1))  # Random positions for crossover points

                descendiente1 = []
                descendiente2 = []
                for i in range(len(individuo1.individuo)):
                    if i in posiciones_cruza:
                        descendiente1.append(individuo2.individuo[i])
                        descendiente2.append(individuo1.individuo[i])
                    else:
                        descendiente1.append(individuo1.individuo[i])
                        descendiente2.append(individuo2.individuo[i])

                descendientes.append(descendiente1)
                descendientes.append(descendiente2)

            return descendientes

        def mutar_poblacion(self, poblacion, individual_mutation, gene_mutation):

            for i in range(len(poblacion)):
                if random.random() < individual_mutation:
                    poblacion[i] = [1 if bit == 0 else 0 for bit in poblacion[i]]

            for i in range(len(poblacion)):
                for j in range(len(poblacion[i])):
                    if random.random() < gene_mutation:
                        poblacion[i][j] = 1 if poblacion[i][j] == 0 else 0

            return poblacion
        
        def podar_poblacion(self, poblacion_final, limit_population, maximizar):
            # Ordenar poblacion_final según la aptitud de los individuos
            poblacion_final.sort(key=lambda individuo: individuo.fx, reverse=maximizar)
            
            # Mantener solo los primeros limit_population individuos
            poblacion_final = poblacion_final[:limit_population]
            
            return poblacion_final
        
        

        def ejecutar_algoritmo(self, minimo, maximo, delta_deseada, ecuacion, initial_population, limit_population, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar,tree):
            fig, ax = plt.subplots()
            directorio = 'Layout\Models\Generations/'
                    # Crear el directorio si no existe
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            mejores_resultados = []
            promedio_resultados = []
            peores_resultados = []
            mejor_fx = None
            peor_fx = None
            poblacion = self.inicializar_populacion(minimo, maximo, delta_deseada, ecuacion, initial_population)
            insertar_datos(tree, poblacion, es_poblacion_inicial=True)
            
            self.poblacion_final.extend(poblacion)
            
            todas_las_generaciones = []
        
            for _ in range(iteraciones):
                print("calculando generacion num ->", _+1)
                parejas = self.seleccionar_mejores(self.poblacion_final, porcentaje_cruza_value, maximizar) 
                cruza = self.cruzar(parejas)
                poblacion_mutada = self.mutar_poblacion(cruza, individual_mutation, gene_mutation)
                generacion_actual = []
                
                for individuo_binario in poblacion_mutada:
                    mejor_resultado, promedio_resultado, peor_resultado = None, None, None
                    individuo = Individuo(individuo_binario, minimo, maximo, delta_deseada, ecuacion)
                    self.poblacion_final.append(individuo)
                    generacion_actual.append(individuo)
                    
                    if maximizar:
                        mejor_resultado = max(individuo.fx for individuo in self.poblacion_final)
                        peor_resultado = min(individuo.fx for individuo in self.poblacion_final)
                        if mejor_fx is None or mejor_resultado > mejor_fx:
                            mejor_fx = mejor_resultado
                        if peor_fx is None or peor_resultado < peor_fx:
                            peor_fx = peor_resultado
                    else:
                        mejor_resultado = min(individuo.fx for individuo in self.poblacion_final)
                        peor_resultado = max(individuo.fx for individuo in self.poblacion_final)
                        if mejor_fx is None or mejor_resultado < mejor_fx:
                            mejor_fx = mejor_resultado
                        if peor_fx is None or peor_resultado > peor_fx:
                            peor_fx = peor_resultado
                    
                    promedio_resultado = sum(individuo.fx for individuo in self.poblacion_final) / len(self.poblacion_final)      
                    
                poblacion = poblacion_mutada 

                mejores_resultados.append(mejor_resultado)
                promedio_resultados.append(promedio_resultado)
                peores_resultados.append(peor_resultado)
                
                
                todas_las_generaciones.append(generacion_actual)
                print("tiene ",len(todas_las_generaciones), "generaciones")
                
                self.poblacion_final = self.podar_poblacion(self.poblacion_final, limit_population, maximizar)
            
            Graphics.crear_grafica(ecuacion,todas_las_generaciones, directorio,maximizar, xlim=(minimo, maximo), 
                                       ylim=(float(peor_fx), float(mejor_fx)))
            print("Mejor fx:", mejor_fx)
            print("Peor fx:", peor_fx)
            Graphics.crear_video(directorio, "generaciones")
            insertar_datos(tree, self.poblacion_final, es_poblacion_inicial=False)
            x_values = list(range(iteraciones))
            Graphics.update_graph(x_values, mejores_resultados, promedio_resultados, peores_resultados, ax)
            
            print("Población final:")
            for individuo in self.poblacion_final:
                print(individuo.id, individuo.individuo ,individuo.i, individuo.x, individuo.fx)
            

            return self.poblacion_final