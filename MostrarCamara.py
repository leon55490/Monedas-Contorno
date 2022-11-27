# Importar la funcion
import cv2
# Mostrar la camara externa o interna
capturaVideo = cv2.VideoCapture(0)
# Si no detecta una camara decir que no se encontro una camara y salirse del programa
if not capturaVideo.isOpened():
    print("No se enconto una camara")
    exit()
# Mientras detecte la camara
while True:
    # Muestra dos variables y lee la camara
    tipocamara, Camara = capturaVideo.read()
# Pasa el video a una escala de gris
    grises = cv2.cvtColor(Camara, cv2.COLOR_BGR2GRAY)
# Muestra en vivo lo que la camara ve
    cv2.imshow("En vivo", grises)
# Si el programa detecta que presionamos la tecla q, cerrara la camara
# Si no se presiona, se mantendra activa
    if cv2.waitKey(1) == ord("q"):
        break
# Muestra la camara
capturaVideo.release()
# Cierra todas las pestañas abiertas
cv2.destroyAllWindows()
