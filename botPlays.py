import time
import pyautogui
import cv2
import numpy as np
import keyboard
import sys
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# ==========================================
# 1. RUTAS DE BOTONES Y SPRITES (FOTOS)
# ==========================================
BTN_REINICIO  = r"/home/pancho/Documentos/PokelikeBot/Sprites/restarRun.png"
BTN_BATTLE    = r"/home/pancho/Documentos/PokelikeBot/Sprites/battleTower.png"
BTN_GASTLY    = r"/home/pancho/Documentos/PokelikeBot/Sprites/gastly.png"
CATCH_POKEMON = r"/home/pancho/Documentos/PokelikeBot/Sprites/catchPokemon.png"

BTN_KANTO  = r"/home/pancho/Documentos/PokelikeBot/Sprites/kanto.png"
BTN_JOHTO  = r"/home/pancho/Documentos/PokelikeBot/Sprites/johto.png"
BTN_HOENN  = r"/home/pancho/Documentos/PokelikeBot/Sprites/hoenn.png"
BTN_SINNOH = r"/home/pancho/Documentos/PokelikeBot/Sprites/sinnoh.png"
BTN_UNOVA  = r"/home/pancho/Documentos/PokelikeBot/Sprites/unova.png"

DICCIONARIO_REGIONES = {
    "kanto": BTN_KANTO,
    "johto": BTN_JOHTO,
    "hoenn": BTN_HOENN,
    "sinnoh": BTN_SINNOH,
    "unova": BTN_UNOVA
}

LISTA_ENTRENADORES = [
    r"/home/pancho/Documentos/PokelikeBot/Sprites/aceTrainer.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/bugCatcher.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/fireSpitter.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/fisher.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/hiker.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/oldGuy.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/policeman.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/Scientist.png",
    r"/home/pancho/Documentos/PokelikeBot/Sprites/teamRocket.png"
]

MOVE_TUTOR      = r"/home/pancho/Documentos/PokelikeBot/Sprites/moveTutor.png"
POKE_CENTER     = r"/home/pancho/Documentos/PokelikeBot/Sprites/pokeCenter.png"
GRASS           = r"/home/pancho/Documentos/PokelikeBot/Sprites/grass.png"
QUESTION_MARK   = r"/home/pancho/Documentos/PokelikeBot/Sprites/questionMark.png"
MISTERY_TRAINER = r"/home/pancho/Documentos/PokelikeBot/Sprites/misteryTrainer.png"


# ==========================================
# 2. FUNCIONES DE AUTOMATIZACIÓN
# ==========================================

def click_en_imagen(ruta_imagen, timeout=3, confidence=0.8, region_busqueda=(0, 0, 1920, 1080)):
    """
    Busca una imagen en pantalla y hace click en su centro.
    Maneja los argumentos de confianza y región de forma segura.
    """
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            pos = pyautogui.locateCenterOnScreen(ruta_imagen, confidence=confidence, region=region_busqueda)
            if pos is not None:
                pyautogui.click(pos)
                return True
        except (pyautogui.ImageNotFoundException, Exception):
            pass
        time.sleep(0.1)
    return False

def iniciarRun():
    print("Iniciando el bot visual optimizado...")
    time.sleep(1)
    
    # Mitad inferior de tu pantalla de la izquierda
    mitad_inferior = (0, 540, 1920, 540)
    
    print("Buscando 'BATTLE TOWER' únicamente en la mitad inferior de la pantalla...")
    if click_en_imagen(BTN_BATTLE, timeout=5, confidence=0.8, region_busqueda=mitad_inferior):
        print("¡Botón 'Battle Tower' detectado e iniciado!")
    else:
        print("ERROR: No se encontró Battle Tower abajo.")
        sys.exit(0)

    time.sleep(1.5)

    # SELECCIÓN DE REGIÓN
    seleccionRegion = "hoenn"
    print(f"Buscando el botón de la región {seleccionRegion.capitalize()}...")
    ruta_foto_region = DICCIONARIO_REGIONES.get(seleccionRegion, BTN_HOENN)
    
    if click_en_imagen(ruta_foto_region, timeout=4, confidence=0.8):
        print(f"¡Región {seleccionRegion.capitalize()} seleccionada con éxito!")
    else:
        print(f"No encontré el botón de {seleccionRegion}, intentando respaldar con Hoenn...")
        click_en_imagen(BTN_HOENN, timeout=3, confidence=0.8)
    time.sleep(0.5)

    # SELECCIÓN DE POKÉMON INITIAL
    print("Buscando a Gastly en la interfaz...")
    if click_en_imagen(BTN_GASTLY, timeout=4, confidence=0.8):
        print("¡Gastly seleccionado con éxito!")
    else:
        print("ERROR: No encontré la casilla de Gastly en pantalla.")
    time.sleep(1.5)

def buscarPokemon(pokemon_name):
    captura = pyautogui.screenshot()
    texto_limpio = pytesseract.image_to_string(cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2GRAY)).lower()
    return pokemon_name in texto_limpio

def seleccionarFirstPokemon():
    print("Abriendo la Pokébola inicial...")
    
    # NUEVO: Acotamos la búsqueda al área donde aparece la Pokébola inicial en tu juego
    # Región: Arranca en X=150, Y=150 y creamos un recuadro de 300x300 píxeles.
    # Bajamos la confianza a 0.65 para que ignore si tiene texto o ramas encima.
    cuadrante_inicial = (150, 150, 300, 300)
    
    if click_en_imagen(CATCH_POKEMON, timeout=4, confidence=0.65, region_busqueda=cuadrante_inicial):
        print("¡Pokébola detectada visualmente y clickeada!")
    else:
        print("No se encuentra la foto de la Pokébola en el cuadrante inicial.")
        return False
        
    time.sleep(0.8) 

    if buscarPokemon("treecko"):
        print("¡Treecko encontrado en la primera tirada!")
        return True
    else:
        print("Treecko no está. Forzando reinicio de run...")
        
        # Volvemos a buscar la foto en el cuadrante para cerrar el modal si es necesario
        click_en_imagen(CATCH_POKEMON, timeout=2, confidence=0.8, region_busqueda=cuadrante_inicial)
        time.sleep(0.3)
        
        if click_en_imagen(BTN_REINICIO, timeout=4, confidence=0.8):
            print("¡Run reiniciada de forma segura por imagen!")
        time.sleep(1.2) 
        return False

# ==========================================
# 3. CICLO PRINCIPAL
# ==========================================

iniciarRun()
time.sleep(1)
level = 0

while True: 
    if keyboard.is_pressed('ctrl+alt+q'):
        print("¡Bot detenido por el usuario!")
        sys.exit(0)

    if level == 0:
        print("--- [Nivel 1: Fase de Selección] ---")
        if seleccionarFirstPokemon():
            print("¡Objetivo cumplido! Pasando al Nivel 2...")
            level = 1
            
    elif level == 1:
        print("¡Fase 2 Iniciada! El bot frena acá.")
        sys.exit(0)
    
    time.sleep(0.1)