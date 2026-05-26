import pyautogui
import time

print("--- MODO BUSCADOR DE COORDENADAS ---")
print("Posicioná el mouse sobre el objetivo. Control+C en la consola para frenar.\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"Coordenadas actuales -> X: {x}  Y: {y}", end="\r")
        time.sleep(0.15)
except KeyboardInterrupt:
    print("\n\nProceso finalizado con éxito.")