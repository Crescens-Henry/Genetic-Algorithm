import cmath
import re
from sympy import symbols, Eq, sin, solve


def solve_quadratic(a, b, c):
    d = (b**2) - (4*a*c)
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)
    return sol1, sol2


def solve_trigonometric(equation):
    x = symbols('x')
    sol = solve(eval(equation), x)
    return [s.evalf() for s in sol]


def parse_and_solve(equation):
    # Eliminar espacios
    equation = equation.replace(" ", "")

    # Determinar el tipo de ecuación
    if 'sin' in equation or 'cos' in equation or 'tan' in equation:
        return solve_trigonometric(equation)
    else:
        # Extraer coeficientes
        coeficientes = re.findall(r'([+-]?\d*\.?\d*)(x\^2|x)', equation)

        # Asignar coeficientes a, b, c
        a = float(coeficientes[0][0]) if coeficientes[0][0] else 1.0
        b = float(coeficientes[1][0]) if len(
            coeficientes) > 1 and coeficientes[1][0] else 0.0
        c = float(equation.split(
            coeficientes[-1][-1])[-1]) if equation.split(coeficientes[-1][-1])[-1] else 0.0

        return solve_quadratic(a, b, c)
