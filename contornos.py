# importar la funciona
from cv2 import cv2

# Leer la imagen
imagen = cv2.imread('MonedasContorno/contorno.jpg')
# Pasarlo a una escala de gris
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
# Trabajar con la escala de gris, pasarlo a umbral, toca pasarlo a umbral
# para poder trabajar con el
# El _, es para obyener dos variables, una ficticia, ya que el umbral suelta dos valores
# muestra la imgen que se uso y el resultado
_, umbral = cv2.threshold(grises, 100, 255, cv2.THRESH_BINARY)

# Encontrar el contorno, pasarlo a APROX_NONE O APROX_SIMPLE
contorno, jerarquía = cv2.findContours(
    umbral, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar el contorno
cv2.drawContours(imagen, contorno, -1, (163, 52, 240), 5)

# Mostrar
cv2.imshow('imagen original', imagen)
cv2.imshow('imagen en gris', grises)
cv2.imshow('imagen en umbral', umbral)

# El tiempo que se muestra, (0 para imagenes)(1 para videos o camara en vivo)
cv2.waitKey(0)
# Cerrar todas las pestañas al presionar una tecla
cv2.destroyAllWindows()


# APROX_NONE = encuentra todo el contorno, los limites, el contorno completo, un monton de puntos
# APROX_SIMPLE = uriliza menos puntos para encontrar el contorno
