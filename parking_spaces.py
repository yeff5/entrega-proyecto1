import cv2
import numpy as np
import time

def detectar_espacios_libres():
    # Coordenadas de los espacios
    Esp = [
        [500, 20, 80, 190], 
        [650, 20, 80, 190], 
        [800, 20, 80, 190],
        [950, 20, 80, 190], 
        [1090, 20, 80, 190], 
        [1090, 493, 80, 190],
        [950, 493, 80, 190], 
        [800, 494, 80, 190], 
        [650, 494, 80, 190],
        [500, 494, 80, 190]
    ]

    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    inicio = time.time()
    duracion = 3  # segundos

    lista_espacios_libres = []

    while True:
        _, img = video.read()
        if img is None:
            break

        imgs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgTh = cv2.adaptiveThreshold(imgs, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 25, 16)
        imgBlur = cv2.medianBlur(imgTh, 5)
        kernel = np.ones((3, 3), np.int8)
        imgDil = cv2.dilate(imgBlur, kernel)

        lista_espacios_libres = []

        for idx, (x, y, w, h) in enumerate(Esp, start=1):
            recorte = imgDil[y:y + h, x:x + w]
            qtPxBranco = cv2.countNonZero(recorte)

            if qtPxBranco <= 2000:
                lista_espacios_libres.append(idx)

        # Detener después de X segundos
        if time.time() - inicio > duracion:
            break
    
    video.release()
    cv2.imshow('video',img)
    cv2.destroyAllWindows()

    return lista_espacios_libres

# Ejecutar y mostrar los espacios libres
espacios_libres = detectar_espacios_libres()
print("Espacios libres:", espacios_libres)


 