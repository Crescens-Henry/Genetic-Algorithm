import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from Layout.Models import Graphics
import cv2
import imageio
import os
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
from sympy import cos, sin, symbols, rad, sympify
import sympy as sp
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
    

def crear_grafica(ecuacion, lista_generaciones, directorio, maximizar, xlim ,ylim):
    for i, generacion_actual in enumerate(lista_generaciones):
        resultados = [(individuo.x, individuo.fx) for individuo in generacion_actual]

        if maximizar:
            mejor_resultado = max(resultados, key=lambda item: item[1])
            peor_resultado = min(resultados, key=lambda item: item[1])
        else:
            mejor_resultado = min(resultados, key=lambda item: item[1])
            peor_resultado = max(resultados, key=lambda item: item[1])

        otros_resultados = [res for res in resultados if res != mejor_resultado and res != peor_resultado]

        fig = plt.figure(figsize=(10, 5))
        plt.scatter([mejor_resultado[0]], [mejor_resultado[1]], color='g', label='Mejor resultado')
        plt.scatter([peor_resultado[0]], [peor_resultado[1]], color='r', label='Peor resultado')
        plt.scatter([res[0] for res in otros_resultados], [res[1] for res in otros_resultados], color='b', label='Otros resultados')
        
        x = np.linspace(xlim[0], xlim[1], 1000)

        x_symbol = sp.symbols('x')
        ecuacion_sympy = sp.sympify(ecuacion)

        y = [float(ecuacion_sympy.subs(x_symbol, x_val)) for x_val in x]

        plt.plot(x, y, color='k', label='Ecuación')


        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Generacion: ' + str(i+1))
        plt.legend()

        plt.xlim(xlim)
        plt.ylim(ylim)
        if not maximizar:
            plt.gca().invert_yaxis()

        plt.savefig(f'{directorio}/generacion_{i+1}.png')
        plt.close()

def crear_video(directorio, nombre_video):
    imagenes = [img for img in os.listdir(directorio) if img.endswith(".png")]
    imagenes = sorted(imagenes, key=lambda img: int(img.split('generacion_')[1].split('.')[0]))
    frames = []
    for imagen in imagenes:
        frames.append(imageio.imread(f'{directorio}/{imagen}'))
    fps = 5 
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
    
