import pyautogui
import time

print("--- MODO BUSCADOR DE COORDENADAS ---")
print("Posicioná el mouse sobre el objetivo. Control+C en la consola para frenar.\n")

try:
    while True:
        x, y = pyautogui.position()
        # \033[K es el código ANSI que borra la línea desde el cursor hasta el final
        print(f"\033[KCoordenadas actuales -> X: {x}  Y: {y}", end="\r")
        time.sleep(0.15)
except KeyboardInterrupt:
    print("\n\nProceso finalizado con éxito.")