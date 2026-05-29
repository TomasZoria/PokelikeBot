import time
import pyautogui
import cv2
import numpy as np
import keyboard
import sys

# =========================================================================
# 1. TUS COORDENADAS CONFIGURADAS (Eje X original, Ejes Y: 745 y 795)
# =========================================================================
COORD_POKEBOLA = (888, 267)   # <- Dejá acá tu coordenada real de la pokébola
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

SHINY_REFERENCE  = r"C:\Brother\Pancho\Script poke\Sprites\shiny_referencia.png" 

# =========================================================================
# 2. FUNCIONES
# =========================================================================
def buscar_shiny_en_pantalla():
    captura = pyautogui.screenshot()
    captura_np = np.array(captura)
    captura_gris = cv2.cvtColor(captura_np, cv2.COLOR_RGB2GRAY)
    
    plantilla = cv2.imread(SHINY_REFERENCE, 0)
    if plantilla is None:
        print("[!] Alerta: No se encuentra 'shiny_referencia.png'. El bot asume que NO hay shiny.")
        return False
        
    resultado = cv2.matchTemplate(captura_gris, plantilla, cv2.TM_CCOEFF_NORMED)
    umbral_certeza = 0.8  
    coincidencias = np.where(resultado >= umbral_certeza)
    return len(coincidencias[0]) > 0

def hacer_click_doble_zona(coord_alta, coord_baja):
    """Hace un click en la coordenada alta y otro en la baja para asegurar el botón"""
    pyautogui.click(coord_alta)
    time.sleep(0.1)
    pyautogui.click(coord_baja)

def ciclo_de_busqueda():
    print("\n--- Iniciando nuevo intento ---")
    
    # Entrar a la Pokébola
    print("Entrando a la Pokébola...")
    pyautogui.click(COORD_POKEBOLA)
    time.sleep(0.1)  
    
    if buscar_shiny_en_pantalla():
        print("[!!!] ¡SHINY DETECTADO DE ENTRADA!")
        return True 
        
    # Tanda de Rerolls (Ahora hace dos clicks por cada slot: arriba y abajo)
    print("No hay shiny de entrada. Probando Rerolls...")
    
    # Slot 1
    print("Reroll Slot 1...")
    hacer_click_doble_zona(REROLL_1_ALTO, REROLL_1_BAJO)
    time.sleep(0)
    if buscar_shiny_en_pantalla(): return True

    # Slot 2
    print("Reroll Slot 2...")
    hacer_click_doble_zona(REROLL_2_ALTO, REROLL_2_BAJO)
    time.sleep(0)
    if buscar_shiny_en_pantalla(): return True

    # Slot 3
    print("Reroll Slot 3...")
    hacer_click_doble_zona(REROLL_3_ALTO, REROLL_3_BAJO)
    time.sleep(0)
    if buscar_shiny_en_pantalla(): return True

    # =========================================================================
    # SOLUCIÓN A LA 'R': Forzar foco con click e intentar dos métodos de teclado
    # =========================================================================
    print("No hubo suerte. Reiniciando run...")
   
    print("Entrando a la Pokébola...")
    pyautogui.click(COORD_POKEBOLA)
    time.sleep(0.1) 
   
       # Reniciar RUN
    print("Reiniciando run...")
    pyautogui.click(COORD_REINICIO)
    time.sleep(0.1)
    
    # Esperamos a que el mapa cargue de cero
    time.sleep(0.2) 
    return False

# =========================================================================
# 3. BUCLE PRINCIPAL
# =========================================================================
bot_activo = False
ejecutando_ciclo = False

def alternar_bot():
    global bot_activo
    if not bot_activo:
        bot_activo = True
        print("\n[PLAY] >>> BOT ACTIVADO. Empezando a trabajar...")
    else:
        bot_activo = False
        print("\n[PAUSE] ||| BOT PAUSADO. Presioná Ctrl+Alt+S para reanudar.")

def salir_del_script():
    print("\n[STOP] !!! Cerrando el script por completo de forma segura...")
    sys.exit(0)

if __name__ == "__main__":
    print("====================================================")
    print("             BOT POKELIKE PREPARADO                 ")
    print("====================================================")
    print(" > [Ctrl + Alt + S] -> Iniciar / Pausar el Bot")
    print(" > [Ctrl + Alt + Q] -> Cerrar el Script por completo")
    print("====================================================")
    print("Esperando tus teclas para empezar en el juego...\n")

    # Registramos los atajos de teclado globales
    keyboard.add_hotkey('ctrl+alt+s', alternar_bot)
    keyboard.add_hotkey('ctrl+alt+q', salir_del_script)

    intentos = 0

    while True: # Bucle infinito para que nunca se cierre solo
        if bot_activo and not ejecutando_ciclo:
            ejecutando_ciclo = True
            intentos += 1
            print(f"\n>> INTENTO Nº {intentos}")
            
            # Ejecuta el ciclo y devuelve True si encontró un Shiny
            shiny_encontrado = ciclo_de_busqueda()
            
            ejecutando_ciclo = False
            
            if shiny_encontrado:
                bot_activo = False # <--- ACÁ SE PAUSA: Cambiamos el estado a falso para que no siga clickeando
                
                print("\n==============================================")
                print("¡¡¡SHINY ENCONTRADO!!! El bot se ha PAUSADO.")
                print("Revisá tu juego. Presioná Ctrl+Alt+S si querés continuar.")
                print("==============================================")
                
                
        # Evita el consumo excesivo de procesador en espera
        time.sleep(0.1)