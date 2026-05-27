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

# --- LISTA ORDENADA DE ÍTEMS PARA EL CAMINO ---
LISTA_ITEMS_CAMINO = [
    (888, 267),
    (848, 359),  
    (824, 461),  
    (850, 572),  
    (825, 660),  
    (850, 764),  
    (893, 864),  
    (1012, 967)  
]
# Variable global para saber qué ítem toca elegir en el lobby
indice_item_actual = 0 

SKIP_ITEM = (965, 660)
SHINY_MARK = (954, 805)

# POKÉMONES
COORD_GASTLY = (726, 258)
COORD_SCYTHER = (820, 257)
COORD_CHARMANDER = (915, 263)

TREECKO_IMG      = r"C:\Brother\Pancho\Script poke\Sprites\treecko.png"
FIRST_MT         = r"C:\Brother\Pancho\Script poke\Sprites\firstMT.png"
SECOND_MT        = r"C:\Brother\Pancho\Script poke\Sprites\secondMT.png"
SHINY_REFERENCE = r"C:\Brother\Pancho\Script poke\Sprites\shiny_referencia.png"

DETECTION_IMG = {
    "item_found":     r"C:\Brother\Pancho\Script poke\Sprites\itemFound.png",
    "move_tutor":     r"C:\Brother\Pancho\Script poke\Sprites\moveTutor.png",
    "shiny_detected": r"C:\Brother\Pancho\Script poke\Sprites\shinyMark.png",
    "trainer_fight":  r"C:\Brother\Pancho\Script poke\Sprites\trainerFight.png",
    "wild_pokemon":   r"C:\Brother\Pancho\Script poke\Sprites\wildPokemon.png",
    "lobby_image" :   r"C:\Brother\Pancho\Script poke\Sprites\Lobby.png",
    "catch_pokemon" : r"C:\Brother\Pancho\Script poke\Sprites\catchPokemon.png"
}

# ==========================================
# 2. FUNCIONES
# ==========================================

def iniciarRun():
    global indice_item_actual, mt
    print("Iniciando el bot...")
    
    # RESETEO DE VARIABLES PARA LA NUEVA RUN
    indice_item_actual = 0
    mt = 1
    
    time.sleep(2)
    
    if battleTower():
        print("¡Estamos en la Battle Tower! Iniciando batalla...")
        pyautogui.click(COORD_BATTLE)
    else:
        print("Detectado botón 'Continue'. Presionando...")
        pyautogui.click(COORD_BATTLECONTINUE)   
    
    time.sleep(0.5)
    
    seleccionRegion = "hoenn"
    coordenadaClick = region(seleccionRegion)
    
    print(f"Seleccionando región {seleccionRegion.capitalize()}...")
    pyautogui.click(coordenadaClick)
    time.sleep(0.5)

    print("Seleccionando Scyther...")
    pyautogui.click(COORD_SCYTHER)
    time.sleep(0.5)

def battleTower():
    captura = pyautogui.screenshot()
    captura_np = np.array(captura)
    captura_gris = cv2.cvtColor(captura_np, cv2.COLOR_RGB2GRAY)
    texto_extraido = pytesseract.image_to_string(captura_gris)
    return "continue" not in texto_extraido.lower()
    
def hacer_click_doble_zona(coord_alta, coord_baja):
    pyautogui.click(coord_alta)
    time.sleep(0.1)
    pyautogui.click(coord_baja)

def region(region_name):
    captura = pyautogui.screenshot()
    captura_np = np.array(captura)
    captura_gris = cv2.cvtColor(captura_np, cv2.COLOR_RGB2GRAY)
    texto_extraido = pytesseract.image_to_string(captura_gris)

    if region_name in texto_extraido.lower():
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
        return encontrado is not None
    except pyautogui.ImageNotFoundException:
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
    except Exception:
        return None

def Reroll(ruta_imagen):
    for i, (alta, baja) in enumerate([(REROLL_1_ALTO, REROLL_1_BAJO), (REROLL_2_ALTO, REROLL_2_BAJO), (REROLL_3_ALTO, REROLL_3_BAJO)], 1):
        print(f"Reroll Slot {i}...")
        hacer_click_doble_zona(alta, baja)
        time.sleep(0.2)
        if buscarPokemon(ruta_imagen): 
            return True
    return False

def seleccionarFirstPokemon():
    print("Abriendo la Pokébola inicial...")
    pyautogui.click(COORD_POKEBOLA)
    time.sleep(0.3)

    treecko_asegurado = False

    # 1. Intentar encontrar a Treecko (a la primera o en Reroll)
    if buscarPokemon(TREECKO_IMG):
        print("¡Treecko encontrado a la primera!")
        treecko_asegurado = True
    else:
        print("Treecko no está. Iniciando Rerolls...")
        if Reroll(TREECKO_IMG):
            print("¡Treecko encontrado en el reroll!")
            treecko_asegurado = True

    # 2. Si logramos asegurar a Treecko, buscamos su posición para clickearlo
    if treecko_asegurado:
        pos = buscarMT(TREECKO_IMG)
        if pos is not None:
            print("¡Posición de Treecko encontrada! Clickeando...")
            punto_central = pyautogui.center(pos)
            pyautogui.click(punto_central)
            time.sleep(0.2)
        else:
            print("¡Alerta! Se detectó a Treecko pero no se pudo obtener su posición en pantalla.")
        return True

    # 3. Si todo falló, reiniciamos la run
    else:
        print("No hubo suerte en los rerolls. Reiniciando run...")
        pyautogui.click(COORD_POKEBOLA)
        time.sleep(0.2) 
    
        print("Haciendo click en Reinicio...")
        pyautogui.click(COORD_REINICIO)     
        time.sleep(0.5) 
        return False

def getEstado():
    for nombre_estado, ruta in DETECTION_IMG.items():
        if buscarPokemon(ruta):
            return nombre_estado
    return "explorando"

def loopJugable():
    global indice_item_actual, mt
    estado = getEstado()
    
    match estado:
        case "item_found":
            print("Item encontrado...")
            pyautogui.click(SKIP_ITEM)
            time.sleep(0.5)
        
        case "move_tutor":
            print("MT...")
            if mt == 1:
                posicion_mt = buscarMT(FIRST_MT)
                if posicion_mt is not None:
                    print("¡Botón de X-Scissor encontrado! Clickeando...")
                    punto_central = pyautogui.center(posicion_mt)
                    pyautogui.click(punto_central)
                    mt += 1
            else:
                posicion_mt = buscarMT(SECOND_MT)
                if posicion_mt is not None:
                    print("¡Botón de Megahorn encontrado! Clickeando...")
                    punto_central = pyautogui.center(posicion_mt)
                    pyautogui.click(punto_central)
            time.sleep(0.5)

        case "shiny_detected":
            print("SHINY!!")
            pyautogui.click(SHINY_MARK)
            time.sleep(0.5)

        case "trainer_fight":
            print("Peleando contra un entrenador...")
            time.sleep(1)

        case "wild_pokemon":
            print("Peleando contra un pokemon salvaje...")
            time.sleep(1)

        case "catch_pokemon": 
            print("Seleccionando un pokemon...")
            shiny_asegurado = False

            if (buscarPokemon(SHINY_REFERENCE)):
                print("Shiny asegurado")
                shiny_asegurado = True
            else:
                print("Iniciando Rerolls")
                if(Reroll(SHINY_REFERENCE)):
                    print("Shiny encontrado!")
                    shiny_asegurado = True

            if shiny_asegurado:
                pos_shiny = buscarMT(SHINY_REFERENCE)
                if pos_shiny is not None:
                    print("¡Haciendo click en el Pokémon Shiny!")
                    punto_central = pyautogui.center(pos_shiny)
                    pyautogui.click(punto_central)
                else:
                    print("Error: Se detectó el Shiny pero se perdió su posición. Clickeando por defecto...")
                    pyautogui.click(COORD_POKEBOLA)
            
            else:
                print("No salió ningún Shiny en los rerolls. Avanzando con Pokémon normal...")
                pyautogui.click(COORD_POKEBOLA)
            


            time.sleep(1)

        case "lobby_image":
            if indice_item_actual < len(LISTA_ITEMS_CAMINO):
                coordenada_click = LISTA_ITEMS_CAMINO[indice_item_actual]
                print(f"Lobby detectado. Seleccionando fase/item número {indice_item_actual + 1} en {coordenada_click}...")
                pyautogui.click(coordenada_click)
                
                # Avanzamos el índice para que en el próximo lobby elija el siguiente ítem
                indice_item_actual += 1
            else:
                print("Se alcanzaron todas las fases de la lista.")
                indice_item_actual = 0
            
            # Una pausa crucial para evitar que vuelva a detectar 'lobby_image' antes de que cambie la pantalla
            time.sleep(1.0) 

        case _:
            # Para evitar sobrecargar la CPU cuando está "explorando"
            time.sleep(0.2)

# ==========================================
# 3. CICLO PRINCIPAL
# ==========================================
iniciarRun()
level = 1


while True:
    # Botón de pánico global
    if keyboard.is_pressed('ctrl+alt+q'):
        print("¡Bot detenido por el usuario!")
        sys.exit(0)

    print(f"--- Intentando preparar Nivel {level} ---")

    if seleccionarFirstPokemon():
        print(f"¡Treecko asegurado! Procediendo a jugar el nivel {level}...")
        level += 2
        time.sleep(1)
    else:
        print("Falló el proceso para asegurar Treecko. Reintentando run completa...")
        time.sleep(1)
        continue

    # Bucle del juego activo
    while level > 1:
        if keyboard.is_pressed('ctrl+alt+q'):
            print("¡Bot detenido por el usuario!")
            sys.exit(0)
        
        loopJugable()