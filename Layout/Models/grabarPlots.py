import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2 as cv
import numpy as np
import os


def animarPlot(x,y):    
    fig,ax = plt.subplots();    
    def actualizarPlot(i):
        ax.clear()        
        ax.scatter(x[:i],y[:i])
        if y[:i]:  # Verificar que la lista no esté vacía
            try:
                ymin = np.min([val for val in y[:i] if np.isfinite(val)])  # Solo considerar valores finitos
                ymax = np.max([val for val in y[:i] if np.isfinite(val)])  # Solo considerar valores finitos
                ax.set_xlim([1.1*np.min(x),1.1*np.max(x)])
                epsilon = 0.01  # o cualquier valor pequeño
                ax.set_ylim([1.1*ymin - epsilon, 1.1*ymax + epsilon])
            except TypeError:
                print("La lista y contiene valores no numéricos.")
    animar = FuncAnimation(fig, actualizarPlot,range(len(x)),interval=0, cache_frame_data=False, repeat = False)
    print ("intenta animar el plot")
    return fig, animar

def grabarVideo(animacion,nombre_video):
        fig, animar = animacion
        animar.save(nombre_video,writer = 'ffmpeg',fps = 60, dpi = 100)
        plt.close(fig)

def unirVariosVideos(listaAnimaciones,listaVideos):
    videos = []
    for i in range(len(listaAnimaciones)):
        fig,animar = listaAnimaciones[i]       
        animar.save(listaVideos[i],writer = 'ffmpeg', fps = 60, dpi=100)
        plt.close(fig)
        videos.append(cv.VideoCapture(listaVideos[i]))

    ancho = int(videos[0].get(cv.CAP_PROP_FRAME_WIDTH))
    alto = int(videos[0].get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(videos[0].get(cv.CAP_PROP_FPS))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video_combinado = cv.VideoWriter('video_final.mp4', fourcc, fps,(ancho,alto))    

    for video in videos:
        while True:
            ret, frame = video.read()
            if not ret:
                break
            video_combinado.write(frame)  # Escribe el frame en el video combinado
        video.release()  # Asegúrate de liberar el video antes de eliminarlo

    video_combinado.release()  # No olvides liberar el video combinado al final

def reproducirVideo(nombre_video):
    video = cv.VideoCapture(nombre_video)
    while True:
        ret, frame = video.read()
        if not ret:
            break
        cv.imshow('Video Final', frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    video.release()
    cv.destroyAllWindows()