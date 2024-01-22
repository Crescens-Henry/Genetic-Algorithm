import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Layout.Models import Graphics
import cv2
import imageio
import os
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
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
    plt.show()
    

def crear_grafica(generacion_actual, directorio, generacion, maximizar):
    # Obtén los valores fx y x de todos los individuos en la generación actual
    resultados = [(individuo.x, individuo.fx) for individuo in generacion_actual]

    # Determina el mejor y el peor resultado en función del botón que se haga clic
    if maximizar:
        mejor_resultado = max(resultados, key=lambda item: item[1])
        peor_resultado = min(resultados, key=lambda item: item[1])
    else:
        mejor_resultado = min(resultados, key=lambda item: item[1])
        peor_resultado = max(resultados, key=lambda item: item[1])

    # Filtra los valores que no son ni el mínimo ni el máximo
    otros_resultados = [res for res in resultados if res != mejor_resultado and res != peor_resultado]

    fig = plt.figure(figsize=(10, 5))
    plt.scatter([mejor_resultado[0]], [mejor_resultado[1]], color='g', label='Mejor resultado')
    plt.scatter([peor_resultado[0]], [peor_resultado[1]], color='r', label='Peor resultado')
    plt.scatter([res[0] for res in otros_resultados], [res[1] for res in otros_resultados], color='b', label='Otros resultados')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Generacion: ' + str(generacion))
    plt.legend()
    plt.savefig(f'{directorio}/generacion_{generacion}.png')
    plt.close()

def crear_video(directorio, nombre_video):
    imagenes = [img for img in os.listdir(directorio) if img.endswith(".png")]
    imagenes.sort()
    frames = []
    for imagen in imagenes:
        frames.append(imageio.imread(f'{directorio}/{imagen}'))
    fps = 10  # Ajusta este valor para cambiar la duración del video
    imageio.mimsave(f'{nombre_video}.mp4', frames, fps=fps)

def ejecutar_video(nombre_video):
    video = cv2.VideoCapture(f'{nombre_video}.mp4')
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    # cv2.destroyAllWindows()
    
