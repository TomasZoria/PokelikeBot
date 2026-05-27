import pyautogui
import time
import keyboard

cambio = True
while cambio == True:
    if keyboard.is_pressed('enter'):
        print(pyautogui.position())
        time.sleep(1)

    if keyboard.is_pressed('m'):
        cambio = False

    # Arriba izquierda 740, 120
    # Abajo derecha 1270, 1000
    # Ancho 530
    # Alto 880


    #Shiny on Question =    954, 805

