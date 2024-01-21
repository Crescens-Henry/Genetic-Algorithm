import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Layout.Models import LineChart



# En el módulo donde se define update_graph
def update_graph(x_values, mejores_resultados, promedio_resultados, peores_resultados, ax):
    ax.clear()
    ax.plot(x_values, mejores_resultados, label='Mejor resultado')
    ax.plot(x_values, promedio_resultados, label='Promedio de resultados')
    ax.plot(x_values, peores_resultados, label='Peor resultado')
    ax.legend()
    ax.set_title('Evolución de los Resultados por Iteración')
    ax.set_xlabel('Generaciones')
    ax.set_ylabel('Aptitud')
