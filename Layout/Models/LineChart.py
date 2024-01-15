import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


def update_graph(x_values, y_values1, y_values2, y_values3, ax):
    ax.clear()
    ax.plot(x_values, y_values1, label='Data 1')
    ax.plot(x_values, y_values2, label='Data 2')
    ax.plot(x_values, y_values3, label='Data 3')
    ax.legend()
    ax.set_title('Fluctuación de Datos en Tiempo Real')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Valor')
