import time
import pyautogui
import cv2
import numpy as np
import keyboard
import sys
import pytesseract

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Brother\Pancho\tesseract.exe"

# ==========================================
# 1. COORDS Y FOTOS
# ==========================================
COORD_POKEBOLA = (888, 267)
COORD_REINICIO = (1885, 140)

# Rerolls
REROLL_1_ALTO = (700, 745)
REROLL_1_BAJO = (700, 795)
REROLL_2_ALTO = (960, 745)
REROLL_2_BAJO = (960, 795)
REROLL_3_ALTO = (1210, 745)
REROLL_3_BAJO = (1210, 795)

# MENÚ
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

COORD_ITEM1 = (848, 359)
COORD_ITEM2 = (824, 461)
COORD_ITEM3 = (850, 572)
COORD_ITEM4 = (825, 660)
COORD_ITEM5 = (850, 764)
COORD_ITEM6 = (893, 864)
COORD_ITEM7 = (1012, 967)

SKIP_ITEM = (965, 660)
SHINY_MARK = (954, 805)

# POKÉMONES
COORD_GASTLY = (726, 258)
COORD_SCYTHER = (820, 257)
COORD_CHARMANDER =  (915, 263)


LISTA_ENTRENADORES = [
    r"C:\Brother\Pancho\Script poke\Sprites\aceTrainer.png",
    r"C:\Brother\Pancho\Script poke\Sprites\bugCatcher.png",
    r"C:\Brother\Pancho\Script poke\Sprites\fireSpitter.png",
    r"C:\Brother\Pancho\Script poke\Sprites\fisher.png",
    r"C:\Brother\Pancho\Script poke\Sprites\hiker.png",
    r"C:\Brother\Pancho\Script poke\Sprites\oldGuy.png",
    r"C:\Brother\Pancho\Script poke\Sprites\policeman.png",
    r"C:\Brother\Pancho\Script poke\Sprites\Scientist.png",
    r"C:\Brother\Pancho\Script poke\Sprites\teamRocket.png"
]
TREECKO_IMG     = r"C:\Brother\Pancho\Script poke\Sprites\treecko.png"
SHINY_REFERENCIA = r"C:\Brother\Pancho\Script poke\Sprites\shiny_referencia.png"

FIRST_MT        = r"C:\Brother\Pancho\Script poke\Sprites\firstMT.png"
SECOND_MT       = r"C:\Brother\Pancho\Script poke\Sprites\secondMT.png"

DETECTION_IMG = {
    "item_found":    r"C:\Brother\Pancho\Script poke\Sprites\itemFound.png",
    "move_tutor":    r"C:\Brother\Pancho\Script poke\Sprites\moveTutor.png",
    "shiny_detected": r"C:\Brother\Pancho\Script poke\Sprites\shinyMark.png",
    "trainer_fight": r"C:\Brother\Pancho\Script poke\Sprites\trainerFight.png",
    "wild_pokemon":  r"C:\Brother\Pancho\Script poke\Sprites\wildPokemon.png",
    "lobby_image" :  r"C:\Brother\Pancho\Script poke\Sprites\Lobby.png",
    "catch_pokemon" : r"C:\Brother\Pancho\Script poke\Sprites\catchPokemon.png"
 }


# ==========================================
# 2. FUNCIONES
# ==========================================

def iniciarRun():
    print("Iniciando el bot...")
    time.sleep(2)
    
    if battleTower():
        print("¡Estamos en la Battle Tower! Iniciando batalla...")
        pyautogui.click(COORD_BATTLE)
    else:
        print("Detectado botón 'Continue'. Presionando...")
        pyautogui.click(COORD_BATTLECONTINUE)   
    
    time.sleep(0.5) # Esperar a que abra el menú de regiones
    
    # REGIÓN A JUGAR
    seleccionRegion = "hoenn"
    coordenadaClick = region(seleccionRegion)
    
    print(f"Seleccionando región {seleccionRegion.capitalize()}...")
    pyautogui.click(coordenadaClick)
    time.sleep(0.5)

    # POKÉMON ELEGIDO
    print("Seleccionando Charmander...")
    pyautogui.click(COORD_SCYTHER)
    time.sleep(0.5)


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

    if region_name in texto_limpio:
        return MAPA_REGIONES[region_name]
    else:
        return COORD_HOENN
    
def buscarPokemon(imagen, confidence=0.8, region=None):
    try:
        encontrado = pyautogui.locateOnScreen(
            imagen,
            confidence=confidence,
            region=region,
            grayscale=True
        )

        if encontrado is not None:
            return True
            
    except pyautogui.ImageNotFoundException:
        return False
        
    return False

def buscarMT(imagen, confidence=0.8, region=None):
    try:
        encontrado = pyautogui.locateOnScreen(
            imagen,
            confidence=confidence,
            region=region,
            grayscale=True
        )

        return encontrado 
            
    except pyautogui.ImageNotFoundException:
        return None
    except Exception: # Por si ocurre otro error aleatorio
        return None


def Reroll(ruta_imagen):
    # Slot 1
    print("Reroll Slot 1...")
    hacer_click_doble_zona(REROLL_1_ALTO, REROLL_1_BAJO)
    time.sleep(0.2) # Pausa para que la pantalla reaccione
    if buscarPokemon(ruta_imagen): return True

    # Slot 2
    print("Reroll Slot 2...")
    hacer_click_doble_zona(REROLL_2_ALTO, REROLL_2_BAJO)
    time.sleep(0.2)
    if buscarPokemon(ruta_imagen): return True

    # Slot 3
    print("Reroll Slot 3...")
    hacer_click_doble_zona(REROLL_3_ALTO, REROLL_3_BAJO)
    time.sleep(0.2)
    if buscarPokemon(ruta_imagen): return True

    return False


def seleccionarFirstPokemon():
    print("Abriendo la Pokébola inicial...")
    pyautogui.click(COORD_POKEBOLA)
    time.sleep(0.3)

    # CORRECCIÓN: Pasamos la variable de la ruta de la imagen
    if buscarPokemon(TREECKO_IMG):
        print("¡Treecko encontrado a la primera!")
        return True
    else:
        print("Treecko no está. Iniciando Rerolls...")
        if Reroll(TREECKO_IMG):
            print("¡Treecko encontrado en el reroll!")
            return True
        else:
            print("No hubo suerte en los rerolls. Reiniciando run...")
            
            print("Abriendo la Pokébola para poder reiniciar...")
            pyautogui.click(COORD_POKEBOLA)
            time.sleep(0.2) 
        
            print("Haciendo click en Reinicio...")
            pyautogui.click(COORD_REINICIO)     
            time.sleep(0.2) 
            return False

def getEstado():
    for nombre_estado, ruta in DETECTION_IMG.items():
        if buscarPokemon(ruta):
            return nombre_estado
            
    return "explorando" # Si no encuentra ninguna pantalla conocida


def loopJugable():
    estado = getEstado()
    
    match estado:
        case "item_found":
            print("Item encontrado...")
            pyautogui.click(SKIP_ITEM)
        
        case "move_tutor":
            print("MT...")
            if mt == 1 :
                posicion_mt = buscarMT(FIRST_MT)
                if posicion_mt is not None:
                    print("¡Botón de X-Scissor encontrado! Clickeando...")
                    
                    # Obtenemos el centro del botón y hacemos clic
                    punto_central = pyautogui.center(posicion_mt)
                    pyautogui.click(punto_central)

                    mt += 1
            else:
                posicion_mt = buscarMT(SECOND_MT)
                if posicion_mt is not None:
                    print("¡Botón de Megahorn encontrado! Clickeando...")
                    
                    # Obtenemos el centro del botón y hacemos clic
                    punto_central = pyautogui.center(posicion_mt)
                    pyautogui.click(punto_central)


        case "shiny_detected":
            print("SHINY!!")
            pyautogui.click(SHINY_MARK)

        case "trainer_fight":
            print ("Peleando contra un entrenador...")

        case "wild_pokemon":
            print("Peleando contra un pokemon salvaje...")

        case "catch_pokemon": 
            print("Seleccionando un pokemon")

        case "lobby_image":
            print("Seleccionando camino...")

        case "final_boss":
            print("Jefe de acto...")

        case _:
            print("Estado desconocido")



    
# 3. CICLO PRINCIPAL CORREGIDO

iniciarRun()
level = 1
mt = 1

while True: 
    # Botón de pánico
    if keyboard.is_pressed('ctrl+alt+q'):
        print("¡Bot detenido por el usuario!")
        sys.exit(0)

    print(f"--- Intentando preparar Nivel {level} ---")

    if level == 1:
        if seleccionarFirstPokemon():
         print(f"¡Treecko asegurado! Procediendo a jugar el nivel {level}...")
         level += 1
        time.sleep(1)
    else:
        print(f"Falló el proceso para asegurar Treecko. Reiniciando nivel {level}...")
        continue

    while level > 1:
        if keyboard.is_pressed('ctrl+alt+q'):
            print("¡Bot detenido por el usuario!")
            sys.exit(0)
       
        else:
         loopJugable()
       


    time.sleep(0.1)