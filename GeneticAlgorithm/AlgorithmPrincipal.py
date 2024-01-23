import math
import random
import time
from matplotlib import pyplot as plt
import numpy as np
from sympy import cos, sin, symbols, rad, sympify
import sympy as sp
from Layout.Models import LineChart 
from Layout.Models.grabarPlots import animarPlot, grabarVideo, unirVariosVideos, reproducirVideo
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
            # Verificar si la ecuación contiene alguna función trigonométrica
            x_value = self.x
            # Convertir la ecuación a una expresión sympy y sustituir la variable por su valor
            resultado = sympify(ecuacion).subs(var, x_value)
            # Evaluar la expresión
            resultado = resultado.evalf()
            print("Resultado de la ecuación:", resultado)
            return resultado
        except Exception as e:
            print("Error al calcular fx:", e)
            return None

class AlgoritmoGenetico:
        def __init__(self, minimo, maximo, delta_deseada,ecuacion,initial_population, limit_population, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar,tree):
            self.poblacion_final = []
            self.ejecutar_algoritmo(minimo, maximo, delta_deseada, ecuacion, initial_population, limit_population, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar,tree)
        
        def inicializar_poblacion(self, minimo, maximo, delta_deseada, ecuacion, initial_population):
            poblacion = []
            for _ in range(initial_population):
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

            while len(mejores_individuos) >= 2:
                mejor_individuo = mejores_individuos[0]
                for otro_individuo in mejores_individuos[1:]:
                    pareja = (mejor_individuo.i, otro_individuo.i)
                    if pareja not in parejas_formadas:
                        parejas_formadas.add(pareja)
                        parejas.append((mejor_individuo, otro_individuo))
                mejores_individuos.remove(mejor_individuo)

            return parejas
        
        def cruzar(self, parejas):
            descendientes = []
            for pareja in parejas:
                individuo1, individuo2 = pareja
                longitud_minima = min(len(individuo1.individuo), len(individuo2.individuo))
                puntos_cruza = random.randint(1, longitud_minima)
                posiciones_cruza = random.sample(range(1, longitud_minima), min(puntos_cruza, longitud_minima - 1))  
                
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
            poblacion_final.sort(key=lambda individuo: individuo.fx, reverse=maximizar)
            
            poblacion_final = poblacion_final[:limit_population]
            
            return poblacion_final
        
        

        def ejecutar_algoritmo(self, minimo, maximo, delta_deseada, ecuacion, initial_population, limit_population, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar,tree):
            fig, ax = plt.subplots()
            t = np.linspace(0,2*np.pi,101)
            listaAnimaciones = []
            listaVideos = []
            inicio = time.time()
            mejores_resultados = []
            promedio_resultados = []
            peores_resultados = []
            poblacion = self.inicializar_poblacion(minimo, maximo, delta_deseada, ecuacion, initial_population)
            insertar_datos(tree, poblacion, es_poblacion_inicial=True)
            
            # Agregar la población inicial a poblacion_final
            self.poblacion_final.extend(poblacion)
        
            for _ in range(iteraciones):
                print("calculando generacion num ->", _+1)
                parejas = self.seleccionar_mejores(self.poblacion_final, porcentaje_cruza_value, maximizar)  # Selecciona de la población final
                cruza = self.cruzar(parejas)
                poblacion_mutada = self.mutar_poblacion(cruza, individual_mutation, gene_mutation)
                
                # Crear nuevos objetos Individuo a partir de la población mutada y agregarlos a poblacion_final
                for individuo_binario in poblacion_mutada:
                    individuo = Individuo(individuo_binario, minimo, maximo, delta_deseada, ecuacion)
                    self.poblacion_final.append(individuo)
                    # Calcular el mejor, el promedio y el peor resultado de la iteración actual
                    if maximizar:
                        mejor_resultado = max(individuo.fx for individuo in self.poblacion_final)
                        peor_resultado = min(individuo.fx for individuo in self.poblacion_final)
                    else:
                        mejor_resultado = min(individuo.fx for individuo in self.poblacion_final)
                        peor_resultado = max(individuo.fx for individuo in self.poblacion_final) 
                    promedio_resultado = sum(individuo.fx for individuo in self.poblacion_final) / len(self.poblacion_final)
                
                x_values_x = [float(individuo.x) for individuo in self.poblacion_final]
                fx_values_y = [float(individuo.fx) for individuo in self.poblacion_final]
                    
                animacion = animarPlot(x_values_x, fx_values_y)
                nombre_video = "video" + str(_+1) + ".mp4"
                listaVideos.append(nombre_video)
                grabarVideo(animacion, nombre_video)
                
                listaAnimaciones.append(animacion)
                if len(listaAnimaciones) == 0:
                    print("No se generaron frames para la animación.")
                
                poblacion = poblacion_mutada  # Actualiza la población con los individuos mutados
                self.poblacion_final = self.podar_poblacion(self.poblacion_final, limit_population, maximizar)

                # Agregar los resultados a las listas
                mejores_resultados.append(mejor_resultado)
                promedio_resultados.append(promedio_resultado)
                peores_resultados.append(peor_resultado)
            
            unirVariosVideos(listaAnimaciones, listaVideos)
            fin = time.time()
            tiempo_ejecucion = fin - inicio
            print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")
            reproducirVideo("video_final.mp4")
            
            insertar_datos(tree, self.poblacion_final, es_poblacion_inicial=False)
            x_values = list(range(iteraciones))
            LineChart.update_graph(x_values, mejores_resultados, promedio_resultados, peores_resultados, ax)
            plt.show() 
            
            
            print("Población final:")
            for individuo in self.poblacion_final:
                print(individuo.id, individuo.individuo ,individuo.i, individuo.x, individuo.fx)
            
            return self.poblacion_final