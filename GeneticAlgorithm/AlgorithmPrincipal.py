import math
import random
from sympy import cos, sin, symbols
import sympy as sp
from Layout.Models.Table import insertar_datos


class Individuo:
    id_counter = 1
    def __init__(self, individuo, i, minimo, maximo, delta_deseada, ecuacion):
        self.id = Individuo.id_counter
        Individuo.id_counter += 1
        self.individuo = individuo  
        self.i = i  
        self.x = self.calcular_x(minimo, maximo, delta_deseada)
        self.fx = self.calcular_fx(ecuacion)
        
    def __str__(self):
        return f"Individuo {self.id}: {self.individuo}, i: {self.i}, x: {self.x}, fx: {self.fx}"

    def calcular_bits (self, minimo, maximo, delta_deseada):
        rango = maximo-minimo
        saltos = math.ceil(rango/delta_deseada)+1
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
        print(delta)
        
        x = minimo + self.i * delta
        
        return float("{:.2f}".format(x))

    def calcular_fx(self, ecuacion):
        try:
            var = sp.symbols('x')
            resultado = sp.sympify(ecuacion).subs(var, math.radians(self.x))
            return float("{:.2f}".format(resultado))
        except Exception as e:
            print("Error al calcular fx:", e)
            return None
    


class AlgoritmoGenetico:
        def __init__(self, minimo, maximo, delta_deseada,ecuacion,initial_population, limit_population, probabilidad_cruce, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar):
            self.ejecutar_algoritmo(minimo, maximo, delta_deseada, ecuacion, initial_population, limit_population, probabilidad_cruce, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar)
        
        def inicializar_populacion(self, minimo, maximo, delta_deseada, ecuacion, initial_population):
            poblacion = []
            for _ in range(initial_population):
                # Generar un número binario aleatorio de longitud n
                bits = Individuo.calcular_bits(self,minimo, maximo, delta_deseada)
                individuo_binario = "".join(str(random.randint(0, 1)) for _ in range(bits))

                # Convertir el número binario a decimal
                i = int(individuo_binario, 2)
                individuo = Individuo(individuo_binario, i, minimo, maximo, delta_deseada, ecuacion)
                individuo.individuo = individuo_binario  # asignar el número binario al individuo

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

            print("Parejas seleccionadas:")
            for i, pareja in enumerate(parejas):
                print(f"Pareja {i+1}: Individuo {pareja[0].i}, Individuo {pareja[1].i}")

            return parejas
        
       
        def ejecutar_algoritmo(self, minimo, maximo, delta_deseada, ecuacion, initial_population, limit_population, probabilidad_cruce, individual_mutation, gene_mutation, iteraciones, porcentaje_cruza_value, maximizar):
            poblacion = self.inicializar_populacion(minimo, maximo, delta_deseada, ecuacion, initial_population)
            print("maximizar->",maximizar)
            generaciones = [poblacion]
            for _ in range(iteraciones):
                print("Generación:", _+1)
                parejas = self.seleccionar_mejores(poblacion, porcentaje_cruza_value, maximizar)
                poblacion = [individuo for pareja in parejas for individuo in pareja]
                # poblacion = self.cruzar_poblacion(poblacion, probabilidad_cruce)
                # poblacion = self.mutar_poblacion(poblacion, individual_mutation, gene_mutation)
                generaciones.append(poblacion) 
            print("Población final:")
            for i, generacion in enumerate(generaciones):
                print(f"Generación {i+1}:")
                for individuo in generacion:
                    print(individuo)
            # insertar_datos(poblacion)
            return generaciones