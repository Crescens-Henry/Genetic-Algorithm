# En la función AlgorithmPrincipal.py

from GeneticAlgorithm.Equations.GeneralEquation import parse_and_solve


def process_equation(equation_value):
    try:
        minimo, maximo = parse_and_solve(equation_value)
        return minimo, maximo
    except Exception as e:
        # Manejar errores, imprimir o registrar el error según sea necesario
        print(f"Error al procesar la ecuación: {e}")
        return None, None
