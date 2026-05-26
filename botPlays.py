import time
import pyautogui
import cv2
import numpy as np
import keyboard
import sys
import pytesseract



pytesseract.pytesseract.tesseract_cmd = r"C:\Brother\Pancho\tesseract.exe"


# 1. COORDS Y FOTOS

COORD_POKEBOLA = (888, 267)
COORD_REINICIO = (1885, 140)

# Primer botón (Reroll 1)
REROLL_1_ALTO = (700, 745)
REROLL_1_BAJO = (700, 795)

# Segundo botón (Reroll 2)
REROLL_2_ALTO = (960, 745)
REROLL_2_BAJO = (960, 795)

# Tercer botón (Reroll 3)
REROLL_3_ALTO = (1210, 745)
REROLL_3_BAJO = (1210, 795)

#MENU
COORD_BATTLE = (960, 570)
COORD_BATTLECONTINUE = (960, 660)
COORD_KANTO = (970, 215)
COORD_JOHTO = (970, 290)
COORD_HOENN = (970, 365)
COORD_SINNOH = (970, 440)
COORD_UNOVA = (970, 515)

MAPA_REGIONES = {
    "kanto": COORD_KANTO,
    "johto": COORD_JOHTO,
    "hoenn": COORD_HOENN,
    "sinnoh": COORD_SINNOH,
    "unova": COORD_UNOVA
}

#POKEMONES
COORD_GASTLY = (726, 258)

#FOTOS
 
LISTA_ENTRENADORES = [r"C:\Brother\Pancho\Script poke\Sprites/aceTrainer.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/bugCatcher.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/fireSpitter.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/fisher.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/hiker.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/oldGuy.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/policeman.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/Scientist.png",
                      r"C:\Brother\Pancho\Script poke\Sprites/teamRocket.png"]

MOVE_TUTOR = r"C:\Brother\Pancho\Script poke\Sprites/moveTutor.png"
POKE_CENTER = r"C:\Brother\Pancho\Script poke\Sprites/pokeCenter.png"
CATCH_POKEMON = r"C:\Brother\Pancho\Script poke\Sprites/catchPokemon.png"
GRASS = r"C:\Brother\Pancho\Script poke\Sprites/grass.png"
QUESTION_MARK = r"C:\Brother\Pancho\Script poke\Sprites/questionMark.png"
MISTERY_TRAINER = r"C:\Brother\Pancho\Script poke\Sprites/misteryTrainer.png"


# 2. FUNCIONES

def iniciarRun():
    print("Iniciando el bot...")
    time.sleep(2)
    
    if (battleTower()):
        print("¡Estamos en la Battle Tower! Iniciando batalla...")
        pyautogui.click(COORD_BATTLE)
    else:
        print("¡Estamos en la Battle Tower! Iniciando batalla...")
        pyautogui.click(COORD_BATTLECONTINUE)   
    
    #REGION A JUGAR
    seleccionRegion = "hoenn"
    coordenadaClick = region(seleccionRegion)
    
    print(f"Seleccionando región {seleccionRegion.capitalize()}...")
    pyautogui.click(coordenadaClick)
    time.sleep(0.1)

    #POKEMON ELEGIDO
    print("Seleccionando Gastly...")
    pyautogui.click(COORD_GASTLY)
    time.sleep(0.1)


def battleTower():
    captura = pyautogui.screenshot()
    captura_np = np.array(captura)
    captura_gris = cv2.cvtColor(captura_np, cv2.COLOR_RGB2GRAY)

    texto_extraido = pytesseract.image_to_string(captura_gris)
    texto_limpio = texto_extraido.lower()

    if "continue" in texto_limpio:
        return False
    else:        
        return True
    
def hacer_click_doble_zona(coord_alta, coord_baja):
    pyautogui.click(coord_alta)
    time.sleep(0.1)
    pyautogui.click(coord_baja)

def region(region_name):
    captura = pyautogui.screenshot()
    captura_np = np.array(captura)
    captura_gris = cv2.cvtColor(captura_np, cv2.COLOR_RGB2GRAY)

    texto_extraido = pytesseract.image_to_string(captura_gris)
    texto_limpio = texto_extraido.lower()

    if (region_name in texto_limpio):
        return MAPA_REGIONES[region_name]
    else:
        return COORD_HOENN
    
def buscarPokemon(pokemon_name):
    captura = pyautogui.screenshot()
    captura_np = np.array(captura)
    captura_gris = cv2.cvtColor(captura_np, cv2.COLOR_RGB2GRAY)

    texto_extraido = pytesseract.image_to_string(captura_gris)
    texto_limpio = texto_extraido.lower()

    if (pokemon_name in texto_limpio):
        return True
    else:
        return False


def Reroll(pokemon_name):
        # Slot 1
    print("Reroll Slot 1...")
    hacer_click_doble_zona(REROLL_1_ALTO, REROLL_1_BAJO)
    if buscarPokemon(pokemon_name): return True

    # Slot 2
    print("Reroll Slot 2...")
    hacer_click_doble_zona(REROLL_2_ALTO, REROLL_2_BAJO)
    if buscarPokemon(pokemon_name): return True

    # Slot 3
    print("Reroll Slot 3...")
    hacer_click_doble_zona(REROLL_3_ALTO, REROLL_3_BAJO)
    if buscarPokemon(pokemon_name): return True

    else: return False



def seleccionarFirstPokemon():
    pyautogui.click(COORD_POKEBOLA)

    if(buscarPokemon("treecko")):
        print("¡Treecko encontrado!")
        sys.exit(0)
    else:
        print("Reroll para encontrar Treecko...")
        if Reroll("clamperl"):
            print("¡Treecko encontrado en el reroll!")
            sys.exit(0)
        else:
             # Reniciar RUN
            print("No hubo suerte. Reiniciando run...")
   
            print("Entrando a la Pokébola...")
            pyautogui.click(COORD_POKEBOLA)
            time.sleep(0.1) 
        
            print("Reiniciando run...")
            pyautogui.click(COORD_REINICIO)
            time.sleep(0.1)
            
            # Esperamos a que el mapa cargue de cero
            time.sleep(0.2) 
            return False
   

    


    


    

# 3. CICLO PRINCIPAL

iniciarRun()
time.sleep(1)
level = 0

while True: 
    if keyboard.is_pressed('ctrl+alt+q'):
        print("¡Bot detenido por el usuario!")
        sys.exit(0)

    if level == 0:
        print("¡Empezando el nivel 1!")
    seleccionarFirstPokemon()
    level += 1

    if level == 1:
        print("¡Empezando el nivel 2!")
    
time.sleep(0.1)
