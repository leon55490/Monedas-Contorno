from cv2 import cv2
# Trabajar con matrices, siempre que se trabaja con camara en vivo se necesitan matrices
import numpy as np


# Crear la funcion y definir los parametros
def ordenarpuntos(puntos):
    # Concatenar matrices y volverlo una lista
    n_puntos = np.concatenate(
        [puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
    # Ordenar coordenadas y
    # al momento de poner la matrices el rango, toca poner un numero demas, si se quiere empezar
    # desde cero, se pone 1, ya que 1-1= 0, si se quiere empezar desde 1, se pone 2
    # 2-1 = 1

    # Definimos el valor 0
    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])
    # Ordenar coordenadas x
    # sin los dos puntos selecciona solo esa matriz, con los dos puntitos,
    # Selecciona todo el rango

    # Definimos el valor 1
    x1_order = y_order[:2]
    # ordenar el valor, sorted es para ordenar matrices
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
    # Definimos los demas valores
    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

    # Toda funcion tiene que devolver un valor siempre
    return[x1_order[0], x1_order[1], x2_order[0], x2_order[1]]


# Sin importar como este la imagen, la reconoce, el area de trabajo
def alineamiento(imagen, ancho, alto):
    imagen_alineada = None
    grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    tipoumbral, umbral = cv2.threshold(grises, 150, 255, cv2.THRESH_BINARY)
    cv2.imshow("Umbral", umbral)
    contorno = cv2.findContours(
        umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contorno = sorted(contorno, key=cv2.contourArea, reverse=True)[:1]
    # Cerrar contorno de los objetos
    for c in contorno:
        # Disminuir el ruido de las curvas
        epsilon = 0.01 * cv2.arcLength(c, True)
        # Aproximacion de las curvas
        appox = cv2.approxPolyDP(c, epsilon, True)
        # Contar objetos dentro de una lista
        if len(appox) == 4:
            puntos = ordenarpuntos(appox)
            # convertir puntos a matrices
            puntos1 = np.float32(puntos)
            # coordenadas, del papel, la parte exterior de la imagem
            puntos2 = np.float32(
                [[0, 0], [ancho, 0], [0, alto], [ancho, alto]])
            # Metodo de perspectiva, que no importa como este girado la camara
            M = cv2.getPerspectiveTransform(puntos1, puntos2)
            imagen_alineada = cv2.warpPerspective(imagen, M, (ancho, alto))
    return imagen_alineada


capturavideo = cv2.VideoCapture(1)

while True:
    tipocamara, camara = capturavideo.read()
    if tipocamara == False:
        break
    # Definir el ancho y alto del area de trabajo
    imagen_A6 = alineamiento(camara, ancho=480, alto=640)
    # Si detecta la imagen, procesarla
    if imagen_A6 is not None:
        # Crear una lista vacia
        puntos = []
        # pasar a escala de gris
        imagen_gris = cv2.cvtColor(imagen_A6, cv2.COLOR_BGR2GRAY)
        # agregar filtro borroso
        blur = cv2.GaussianBlur(imagen_gris, (5, 5), 1)
        # pasar a Umbral
        _, umbral2 = cv2.threshold(
            blur, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
        #cv2.imshow("umbral2", umbral2)
        # Crear contorno
        contorno2 = cv2.findContours(
            umbral2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # dibujar el contorno
        cv2.drawContours(imagen_A6, contorno2, -1, (255, 0, 0), 2)
        # sumar dos monedas
        suma1 = 0.0
        suma2 = 0.0
        # Hacer un recorrido
        for c_2 in contorno2:
            # Segun el area del circulo sabemos que moneda es
            area = cv2.contourArea(c_2)
            # Encontrar el centro del circulo, etiquetas
            Momentos = cv2.moments(c_2)
            # Definir los momentos, crear etiquetas, crear el centro de masa de un objeto
            # son momentos espaciales
            # momento es de ir de un punto a otro, de momento 00 a espacio 1, (0 momento estatico)
            if(Momentos["m00"] == 0):
                Momentos["m00"] = 1.0
            # Crear la cordenada de x
            x = int(Momentos["m10"]/Momentos["m00"])
            # crear la cordenada de y
            y = int(Momentos["m01"]/Momentos["m00"])

            # Detectar la moneda de 200
            # Reconocer el area de la moneda
            if area < 10500 and area > 9600:
                # gregar una fuente al texto
                font = cv2.FONT_HERSHEY_SIMPLEX
                # Poner donnde quiero ubicada la imagen, que va a decir el texto, las cordenadas, la fuente, el tamañano (maximo es 1), el color y el grosor
                cv2.putText(imagen_A6, "200", (x, y),
                            font, 0.75, (0, 255, 0), 2)
                suma1 = suma1 + 0.2
            # Detectar la moneda de 100
            if area < 9600 and area > 7800:
                # gregar una fuente al texto
                font = cv2.FONT_HERSHEY_SIMPLEX
                # Poner donnde quiero ubicada la imagen, que va a decir el texto, las cordenadas, la fuente, el tamañano (maximo es 1), el color y el grosor
                cv2.putText(imagen_A6, "100", (x, y),
                            font, 0.75, (0, 255, 0), 2)
                suma2 = suma2 + 0.1
        # Sumatoria de las monedas
        total = suma1 + suma2
        # Mostrar el resultados
        print("sumatoria total en pesos:", round(total, 2))
        # Mostrar la imagenes

        cv2.imshow("Imagen A6", imagen_A6)
        cv2.imshow("camara", camara)
    if cv2.waitKey(1) == ord('q'):
        break
capturavideo.release()
cv2.destroyAllWindows()
