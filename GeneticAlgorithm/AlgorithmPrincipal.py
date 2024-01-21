import math
import random
from matplotlib import pyplot as plt
from sympy import cos, sin, symbols, rad, sympify
import sympy as sp
from Layout.Models import LineChart
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
            if 'sin' in ecuacion or 'cos' in ecuacion or 'tan' in ecuacion:
                # Convertir self.x a radianes
                x_value = math.radians(self.x)
            else:
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
        
        def inicializar_populacion(self, minimo, maximo, delta_deseada, ecuacion, initial_population):
            poblacion = []
            for _ in range(initial_population):
                # Generar un número binario aleatorio de longitud n
                bits = Individuo.calcular_bits(self, minimo, maximo, delta_deseada)
                individuo_binario = [random.randint(0, 1) for _ in range(bits)]
                
                individuo = Individuo(individuo_binario, minimo, maximo, delta_deseada, ecuacion)

                poblacion.append(individuo)
                print("Individuo creado:")
                print("ID:", individuo.id)
                print("Individuo:", individuo.individuo)
                print("i:", individuo.i)
                print("x:", individuo.x)
                print("fx:", individuo.fx)
                print("--------------------")
            return poblacion
        
        def seleccionar_mejores(self, poblacion, porcentaje_cruce, maximizar):
            # print("Población que estoy recibiendo:")
            # for individuo in poblacion:
            #     print("Individuo (i):", individuo.i)
            #     print("Individuo (fx):", individuo.fx)
            #     print("--------------------")

            poblacion = [x for x in poblacion if not isinstance(x, list)]
            if maximizar:
                poblacion_ordenada = sorted(poblacion, key=lambda x: x.fx, reverse=True)
            else:
                poblacion_ordenada = sorted(poblacion, key=lambda x: x.fx)

            num_seleccionados = int(len(poblacion) * porcentaje_cruce)
            mejores_individuos = poblacion_ordenada[:num_seleccionados]
            parejas = []
            parejas_formadas = set()

            # Mientras haya suficientes individuos para formar una pareja
            while len(mejores_individuos) >= 2:
                # El mejor individuo es siempre el primero de la lista
                mejor_individuo = mejores_individuos[0]
                # Para cada uno de los otros individuos
                for otro_individuo in mejores_individuos[1:]:
                    # Forma una pareja con el mejor individuo
                    pareja = (mejor_individuo.i, otro_individuo.i)
                    # Verifica que la pareja no se haya formado antes
                    if pareja not in parejas_formadas:
                        parejas_formadas.add(pareja)
                        parejas.append((mejor_individuo, otro_individuo))
                # Elimina el mejor individuo de la lista de mejores individuos
                mejores_individuos.remove(mejor_individuo)

            # # Imprime las parejas en la consola
            # for pareja in parejas:
            #     print("Pareja:")
            #     print("Individuo 1 (binario):", pareja[0].individuo)
            #     print("Individuo 1 (i):", pareja[0].i)
            #     print("Individuo 2 (binario):", pareja[1].individuo)
            #     print("Individuo 2 (i):", pareja[1].i)
            #     print("--------------------")

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

                # # Convierte la versión binaria a una cadena de caracteres
                # descendiente1_str = ''.join(map(str, descendiente1))
                # descendiente2_str = ''.join(map(str, descendiente2))

                # # Convierte la versión binaria a decimal
                # descendiente1_decimal = int(descendiente1_str, 2)
                # descendiente2_decimal = int(descendiente2_str, 2)

                # # Imprime los descendientes en la consola
                # print(f"Descendiente 1 (binario): {descendiente1_str}")
                # print(f"Descendiente 1 (decimal): {descendiente1_decimal}")
                # print(f"Descendiente 2 (binario): {descendiente2_str}")
                # print(f"Descendiente 2 (decimal): {descendiente2_decimal}")
                # print("--------------------")

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
            
            mejores_resultados = []
            promedio_resultados = []
            peores_resultados = []
            poblacion = self.inicializar_populacion(minimo, maximo, delta_deseada, ecuacion, initial_population)
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
                    mejor_resultado = max(individuo.fx for individuo in self.poblacion_final)
                    promedio_resultado = sum(individuo.fx for individuo in self.poblacion_final) / len(self.poblacion_final)
                    peor_resultado = min(individuo.fx for individuo in self.poblacion_final)
                
                poblacion = poblacion_mutada  # Actualiza la población con los individuos mutados
                self.poblacion_final = self.podar_poblacion(self.poblacion_final, limit_population, maximizar)

                # Agregar los resultados a las listas
                mejores_resultados.append(mejor_resultado)
                promedio_resultados.append(promedio_resultado)
                peores_resultados.append(peor_resultado)
            # Insertar los resultados de la poda en la tabla
            insertar_datos(tree, self.poblacion_final, es_poblacion_inicial=False)
            x_values = list(range(iteraciones))
            LineChart.update_graph(x_values, mejores_resultados, promedio_resultados, peores_resultados, ax)
            plt.show()  # Asegúrate de llamar a plt.show() para mostrar la gráfica
            
            print("Población final:")
            for individuo in self.poblacion_final:
                print(individuo.id, individuo.individuo ,individuo.i, individuo.x, individuo.fx)
            
            return self.poblacion_final