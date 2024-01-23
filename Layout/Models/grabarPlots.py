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

        ax.set_xlim([1.1*np.min(x),1.1*np.max(x)])
        ax.set_ylim([1.1*np.min(y),1.1*np.max(y)])
    animar = FuncAnimation(fig, actualizarPlot,range(len(x)),interval=0, cache_frame_data=False, repeat = False)
    return fig, animar

def grabarVideo(animacion,nombre_video):
    fig, animar = animacion
    animar.save(nombre_video,writer = 'ffmpeg',fps = 60, dpi = 100)
    plt.close(fig)

def unirVariosVideos(listaAnimaciones, listaVideos):
    videos = []
    for i in range(len(listaAnimaciones)):
        fig, animar = listaAnimaciones[i]
        animar.save(listaVideos[i], writer='ffmpeg', fps=60, dpi=100)
        plt.close(fig)
        video = cv.VideoCapture(listaVideos[i])
        videos.append(video)

    ancho = int(videos[0].get(cv.CAP_PROP_FRAME_WIDTH))
    alto = int(videos[0].get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(videos[0].get(cv.CAP_PROP_FPS))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video_combinado = cv.VideoWriter('video_final.mp4', fourcc, fps, (ancho, alto))

    for video in videos:
        while True:
            ret, frame = video.read()
            if not ret:
                break
            video_combinado.write(frame)
        video.release()  # Libera el objeto VideoCapture después de leer todos los frames

    video_combinado.release()  # Libera el objeto VideoWriter después de escribir todos los frames

    for video_file in listaVideos:
        if os.path.exists(video_file):  # Verifica si el archivo existe antes de intentar eliminarlo
            os.remove(video_file)  # Elimina el archivo de video después de liberar el objeto VideoCapture

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