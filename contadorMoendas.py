# Importar el cv2
from cv2 import cv2
# Importar el nympy
import numpy as np

# Variables para el gaussianBlur
valorGauss = 1
valorKernel = 3

# Leer la imagen
original = cv2.imread("MonedasContorno/monedas.jpg")
# Pasar al escala de gris
gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

# Suavisado, para imagenes borrosas (Camara en vivo por ejemplo)
gauss = cv2.GaussianBlur(gris, (valorGauss, valorGauss), 0)

# Eliminacion de ruidos
canny = cv2.Canny(gauss, 60, 100)

# numpy (organizar las matrices de los pixeles que voy a usar) tomar todos los contornos
kernel = np.ones((valorKernel, valorKernel), np.uint8)

# Elegir que contorno quiero usar, cerrar el contorno
cierre = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

# Encontrar el contorno, pasarlo a APROX_NONE O APROX_SIMPLE, saca dos valores
contorno, jerarquía = cv2.findContours(
    cierre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Mostrar el numero de contornos cerrados, con le cuenta los elementos de contorno
print("monedas encontradas: {}".format(len(contorno)))

# Dibujar el contorno
cv2.drawContours(original, contorno, -1, (163, 52, 240), 4)


# Mostrar resultado
cv2.imshow('Grises', gris)
cv2.imshow('gauss', gauss)
cv2.imshow('canny', canny)
cv2.imshow('cierre', cierre)
cv2.imshow('resultado', original)

# Tiempo que dura la imagen
cv2.waitKey(0)
# Cierre de pestañas
cv2.destroyAllWindows()
