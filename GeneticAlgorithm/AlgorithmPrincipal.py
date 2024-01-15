# En la función AlgorithmPrincipal.py
import random
import re
import time
from GeneticAlgorithm.Equations.GeneralEquation import parse_and_solve


class Individuo:
    def __init__(self, i, x):
        self.i = i
        self.x = x
        self.fx = None


random.seed(time.time())


def generar_poblacion_inicial(initial_population, minimo, maximo, bits, equation):
    rango = maximo - minimo
    print(f"Rango: {rango}")
    delta = rango / (2**bits - 1)
    print(f"Delta: {delta}")
    poblacion = []
    for _ in range(initial_population):
        i = random.randint(1, 31)  # Genera un número aleatorio entre 1 y 31
        x = minimo + i * delta  # Calcular el valor de x
        x = round(x.real, 2)
        individuo = Individuo(i, x)  # Pasar x al constructor de Individuo
        # Calcular el valor de f(x) para este individuo
        individuo.fx = evaluar_funcion(x, equation)
        individuo.fx = round(individuo.fx.real, 2) 
        poblacion.append(individuo)
    # Imprime los valores de 'i', 'x' y 'f(x)' para cada individuo
    print([(individuo.i, individuo.x, individuo.fx)
          for individuo in poblacion])
    return poblacion


def evaluar_funcion(x, equation):
    # Reemplaza 'x' en la ecuación con el valor de x y evalúa la ecuación
    equation = equation.replace('^', '**')  # Cambia '^' a '**'
    # Asegúrate de que haya un '*' antes de 'x'
    equation = re.sub(r'(\d)x', r'\1*'+str(x), equation)
    return eval(equation)


def process_equation(equation_value):
    try:
        minimo, maximo = parse_and_solve(equation_value)
        return minimo.real, maximo.real
    except Exception as e:
        # Manejar errores, imprimir o registrar el error según sea necesario
        print(f"Error al procesar la ecuación: {e}")
        return None, None
