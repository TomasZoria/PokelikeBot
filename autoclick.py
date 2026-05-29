import pyautogui
import time
import keyboard

clickeando = False
print("Autoclicker iniciado. Presiona Enter para activar/desactivar y ESC para salir.")

while True:
    if keyboard.is_pressed('||'):
        clickeando = not clickeando
        if clickeando:
            print("--- Clickeando activado ---")
        else:
            print("--- Clickeando desactivado ---")
        time.sleep(0.1) 

    # Ejecuta el clic si la variable es True
    if clickeando:
        pyautogui.click()   


        time.sleep(0.01)

    # Cierra el programa si se presiona ESC
    if keyboard.is_pressed('esc'):
        print("Saliendo del programa...")
        break