import random
from sympy import cos, sin, symbols
import sympy as sp
from Layout.Models.Table import insertar_datos


class Individuo:
    def __init__(self, id, individuo, i, min_resultado, max_resultado, minimo, maximo, bits, ecuacion):
        self.id = id
        self.individuo = individuo  
        self.i = i  
        self.min_resultado = min_resultado
        self.max_resultado = max_resultado
        self.x = self.calcular_x(minimo, maximo, bits)
        self.fx = self.calcular_fx(ecuacion)

    def calcular_x(self, minimo, maximo, bits):
        rango = maximo - minimo
        delta = rango / (2 ** bits - 1)
        x = minimo + self.i * delta
        
        return "{:.2f}".format(x)

    def calcular_fx(self, ecuacion):
        x = sp.symbols('x')
        resultado = sp.sympify(ecuacion).subs(x, self.x)
        return "{:.2f}".format(resultado)
    
    def obtener_minimo_maximo(ecuacion_str, min_result, max_result):
        x = sp.symbols('x')
        ecuacion = sp.sympify(ecuacion_str)
        
        resultado_min = ecuacion.subs(x, min_result)
        resultado_max = ecuacion.subs(x, max_result)
        
        return resultado_min, resultado_max

    @staticmethod
    def convertir_hijos(hijos, min_resultado, max_resultado, minimo, maximo, bits, ecuacion):
        individuos = []
        for i, hijo in enumerate(hijos):
            id = i
            individuo = hijo
            i = int(''.join(map(str, individuo)), 2)
            individuos.append(Individuo(id, individuo, i, min_resultado, max_resultado, minimo, maximo, bits, ecuacion))
        return individuos


class AlgoritmoGenetico:
    def __init__(self, poblacion_inicial, min_resultado, max_resultado, minimo, maximo, bits, ecuacion):
        self.poblacion = self.inicializar_poblacion(poblacion_inicial, min_resultado, max_resultado, minimo, maximo, bits, ecuacion)

    def inicializar_poblacion(self, poblacion_inicial, min_resultado, max_resultado, minimo, maximo, bits, ecuacion):
        poblacion = []
        for i in range(poblacion_inicial):
            id = i
            individuo = [random.randint(0, 1) for _ in range(bits)]  
            i = int(''.join(map(str, individuo)), 2) 
            poblacion.append(Individuo(id, individuo, i, min_resultado, max_resultado, minimo, maximo, bits, ecuacion))
        return poblacion
    
    def seleccionar_padres(self, poblacion, porcentaje_cruce):
        poblacion_ordenada = sorted(poblacion, key=lambda x: x.fx)
        num_seleccionados = int(len(poblacion) * porcentaje_cruce)
        mejores_individuos = poblacion_ordenada[:num_seleccionados]
        parejas = []
        for i in range(0, len(mejores_individuos), 2):
            pareja = mejores_individuos[i:i+2]
            if len(pareja) == 2:
                parejas.append(pareja)
        print("Parejas seleccionadas:")
        for i, pareja in enumerate(parejas):
            print(f"Pareja {i+1}: Individuo {pareja[0].i}, Individuo {pareja[1].i}")
        return parejas
    
    def cruza(self, parejas, prob_cruza):
        hijos = []
        for pareja in parejas:
            hijo = []
            if random.random() < prob_cruza:
                punto_cruza = random.randint(1, len(pareja[0].individuo) - 1)
                hijo.extend(pareja[0].individuo[:punto_cruza])
                hijo.extend(pareja[1].individuo[punto_cruza:])
                hijos.append(hijo)
        print("Hijos:")
        for i, hijo in enumerate(hijos):
            print(f"Hijo {i+1}: {hijo}")
        return hijos
    
    def mutex(self, hijos, prob_mutacion_individuo, prob_mutacion_gen):
        for hijo in hijos:
            if random.random() < prob_mutacion_individuo:
                for i in range(len(hijo)):
                    if random.random() < prob_mutacion_gen:
                        hijo[i] = 1 if hijo[i] == 0 else 0
        print("Mutación:")
        for i, hijo in enumerate(hijos):
            print(f"Hijo {i+1}: {hijo}")
        return hijos
    
    def ejecutar(self, num_iteraciones, equation_value, min_result, max_result, initial_population_value, entry_prob_cruza_value, limit_population_value, individual_mutation_value, gene_mutation_value, tree):
        porcentaje_cruce = 0.5  # Algunos o todos para cruzar

        for _ in range(num_iteraciones):
            print("Iteración:", _+1)
            minimo, maximo = Individuo.obtener_minimo_maximo(equation_value, min_result, max_result)
            print("minimo",minimo,"maximo:", maximo)

            if _ == 0:
                insertar_datos(tree, self.poblacion)
                print("Población inicial:")
                for individuo in self.poblacion:
                    print(individuo.individuo,individuo.i, individuo.x, individuo.fx)

            seleccionar_padres = self.seleccionar_padres(self.poblacion, porcentaje_cruce)
            cruza = self.cruza(seleccionar_padres, entry_prob_cruza_value)
            mutex = self.mutex(cruza, individual_mutation_value, gene_mutation_value)
            individuos_hijos = Individuo.convertir_hijos(mutex, min_result, max_result, minimo, maximo, 5, equation_value)
            
            insertar_datos(tree, individuos_hijos, es_poblacion_inicial=False)
            self.poblacion.extend(individuos_hijos)  # Agrega los hijos a la población existente

            """ # Si la población se vuelve demasiado grande, puedes eliminar algunos individuos
            if len(self.poblacion) > limit_population_value:
                self.poblacion = self.seleccionar_mejores(self.poblacion, limit_population_value) """
