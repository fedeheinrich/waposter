import re, time, json, random, schedule, os, logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- CONFIGURACIÓN GLOBAL ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
LOG_FILE_PATH = os.path.join(LOG_DIR, "waposter.log")
MESSAGES_PATH = os.path.join(SCRIPT_DIR, "data", "messages.json")
PROFILE_PATH = os.path.join(SCRIPT_DIR, 'WhatsAppBotProfile')
DRIVER_PATH = os.path.join(SCRIPT_DIR, "msedgedriver.exe") 
MAX_WAIT_TIME = 20 # Segundos

# --- SELECTORES XPATH ---
XPATHS = {
    "buscar_chat": '//div[@role="textbox"][@title="Buscar contacto o chat"]',
    "chat_grupo_span": '//span[@title="{group_name}"]',
    "boton_adjuntar": '//div[@role="button"][@aria-label="Adjuntar"]',
    "input_media": '//input[@accept="image/*,video/*"]',
    "input_comentario": '//div[@role="textbox"][@aria-label="Añade un comentario..."]',
    "boton_enviar": '//div[@role="button"][@aria-label="Enviar"]'
}

def setup_logging():
    """Configura el sistema de logging para consola y archivo."""
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging configurado.")

def setup_driver():
    """Configura e inicia el WebDriver de Edge usando el driver local."""
    logging.info(f"Configurando el driver de Edge (local: {DRIVER_PATH})...")
    
    if not os.path.exists(DRIVER_PATH):
        logging.error(f"ERROR CRÍTICO: No se encontró 'msedgedriver.exe'.")
        logging.error(f"Asegúrate de que el archivo esté en: {DRIVER_PATH}")
        exit()

    service = EdgeService(executable_path=DRIVER_PATH)
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"user-data-dir={PROFILE_PATH}")
    options.add_experimental_option("detach", True)
    
    try:
        driver = webdriver.Edge(service=service, options=options)
        driver.get("https://web.whatsapp.com/")
        logging.info("📱 Por favor, escaneá el código QR y luego presioná ENTER...")
        input()
        logging.info("QR escaneado. Iniciando bot...")
        return driver
    except Exception as e:
        logging.error(f"Error al iniciar el driver o WhatsApp Web: {e}")
        logging.error("Asegúrate de que 'msedgedriver.exe' sea compatible con tu versión de Microsoft Edge.")
        exit()

def load_messages():
    """Carga los mensajes desde el archivo JSON."""
    try:
        with open(MESSAGES_PATH, "r", encoding="utf-8") as file:
            grupos = json.load(file)
        logging.info(f"Se cargaron {len(grupos)} grupos desde {MESSAGES_PATH}")
        return grupos
    except FileNotFoundError:
        logging.error(f"ERROR CRÍTICO: No se encontró '{MESSAGES_PATH}'.")
        exit()
    except Exception as e:
        logging.error(f"Error al leer el archivo JSON: {e}")
        exit()

def buscar_y_abrir_grupo(driver, wait, grupo_nombre):
    """
    Busca un grupo por nombre, limpiando automáticamente emojis y
    símbolos antes de buscar para hacerlo más robusto.
    """
    nombre_limpio_final = "" # Inicializar para que esté disponible en el bloque except
    try:
        # --- INICIO DE LA LÓGICA DE LIMPIEZA ---

        # 1. Normalizar espacios (quitar espacios dobles, raros, etc.)
        nombre_con_espacios_norm = " ".join(grupo_nombre.split())
        
        # 2. Quitar emojis, comas y caracteres especiales.
        #    Nos quedamos solo con letras, números, espacios y (./_-)
        nombre_sin_emojis = re.sub(r'[^\w\s\./_-]', '', nombre_con_espacios_norm)
        
        # 3. Volver a normalizar espacios.
        nombre_limpio_final = " ".join(nombre_sin_emojis.split())

        # --- FIN DE LA LÓGICA DE LIMPIEZA ---

        logging.info(f"Procesando grupo (Nombre JSON): '{grupo_nombre}'")
        logging.info(f"Buscando con nombre limpio: '{nombre_limpio_final}'")
        
        buscar_grupo_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, XPATHS["buscar_chat"])
        ))
        buscar_grupo_input.clear()

        # 4. Usar el nombre LIMPIO para la BÚSQUEDA (send_keys)
        buscar_grupo_input.send_keys(nombre_limpio_final)
        time.sleep(2) # Pausa para que la UI de WhatsApp se actualice

        # 5. Construir un selector XPath más robusto
        parts = [part for part in nombre_limpio_final.split() if part]
        if not parts:
            logging.warning(f"El nombre del grupo '{grupo_nombre}' resultó en una cadena vacía. Saltando.")
            return False
            
        conditions = [f"contains(@title, '{part}')" for part in parts]
        xpath_selector_flexible = f"//span[{' and '.join(conditions)}]"

        logging.info(f"Esperando por el selector (flexible): {xpath_selector_flexible}")

        chat_grupo = wait.until(EC.element_to_be_clickable(
            (By.XPATH, xpath_selector_flexible)
        ))
        
        chat_grupo.click()
        logging.info(f"¡Clic exitoso! El título real del elemento era: '{chat_grupo.get_attribute('title')}'")
        return True
    
    except TimeoutException:
        logging.error(f"No se pudo encontrar el grupo con nombre limpio '{nombre_limpio_final}' (Timeout).")
        logging.error(f"El nombre original era: '{grupo_nombre}'")
        logging.error("Verifica que el nombre en el JSON sea correcto y que el grupo sea visible en WhatsApp Web.")
        
        try:
            # Usar wait para más robustez al limpiar
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS["buscar_chat"]))).clear()
            logging.info("Campo de búsqueda limpiado para el siguiente intento.")
        except Exception as e_clear:
            logging.warning(f"No se pudo limpiar el campo de búsqueda tras el error: {e_clear}")
            
        return False
    
    except Exception as e:
        # Usar repr(e) para obtener más detalles del error
        logging.error(f"Error inesperado al buscar el grupo '{grupo_nombre}' (nombre limpio: '{nombre_limpio_final}'): {repr(e)}")
        return False

def enviar_un_mensaje(driver, wait, mensaje_data):
    """Adjunta imagen, escribe texto y envía un único mensaje."""
    try:
        # 1. Abrir boton de adjuntar
        boton_adjuntar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, XPATHS["boton_adjuntar"])
        ))
        boton_adjuntar.click()

        # 2. Subir la imagen
        input_archivo = wait.until(EC.presence_of_element_located(
            (By.XPATH, XPATHS["input_media"])
        ))
        
        ruta_abs_imagen = os.path.join(SCRIPT_DIR, mensaje_data["imagen"])
        if not os.path.exists(ruta_abs_imagen):
            logging.warning(f"  Aviso: No se encontró la imagen en {ruta_abs_imagen}. Saltando este mensaje.")
            driver.get("https://web.whatsapp.com/") # Volver a home para no bloquear el chat
            return False

        logging.info(f"  Adjuntando imagen: {mensaje_data['imagen']}")
        input_archivo.send_keys(ruta_abs_imagen)

        # 3. Escribir la descripcion
        logging.info(f"  Escribiendo texto: {mensaje_data['texto'][:30]}...")
        descripcion = wait.until(EC.element_to_be_clickable(
            (By.XPATH, XPATHS["input_comentario"])
        ))
        descripcion.send_keys(mensaje_data["texto"])
        time.sleep(random.randint(1, 5)) # Pausa "humana"

        # 4. Enviar
        boton_enviar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, XPATHS["boton_enviar"])
        ))
        boton_enviar.click()
        logging.info(f"  ¡Mensaje enviado exitosamente!")
        return True

    except Exception as e:
        logging.error(f"  ❌ Error al enviar el mensaje (imagen: {mensaje_data['imagen']}): {e}")
        logging.info("  Error capturado. Volviendo a home...")
        driver.get("https://web.whatsapp.com/") # Volver a home para estabilizar
        return False

def procesar_envios(driver, grupos, con_delay=True):
    """Función principal que orquesta el envío a todos los grupos."""
    logging.info("--- Iniciando Tarea Programada ---")
    
    if con_delay:
        delay_minutos = random.randint(0, 10)
        if delay_minutos > 0:
            logging.info(f"Retraso aleatorio activado. Esperando {delay_minutos} minutos.")
            time.sleep(delay_minutos * 60)
    
    wait = WebDriverWait(driver, MAX_WAIT_TIME)
    total_grupos = len(grupos)
    
    for i, grupo_data in enumerate(grupos):
        grupo_nombre = grupo_data["grupo"]
        logging.info(f"\n--- Procesando Grupo {i+1}/{total_grupos}: {grupo_nombre} ---")

        if not buscar_y_abrir_grupo(driver, wait, grupo_nombre):
            driver.get("https://web.whatsapp.com/") # Reset para el siguiente grupo
            continue 

        total_mensajes = len(grupo_data["mensajes"])
        for j, mensaje in enumerate(grupo_data["mensajes"]):
            logging.info(f"Enviando mensaje {j+1}/{total_mensajes} a '{grupo_nombre}'...")
            
            if not enviar_un_mensaje(driver, wait, mensaje):
                logging.warning(f"  Saltando el resto de mensajes para '{grupo_nombre}' debido a un error.")
                break 
            
            pausa_msg = random.randint(60, 180)
            logging.info(f"  Pausa 'anti-spam' de {pausa_msg} segundos...")
            time.sleep(pausa_msg)

    logging.info("\n🎉 ¡Todos los grupos procesados! Esperando la próxima ejecución programada.")

# --- EJECUCIÓN DEL SCRIPT ---
def main():
    setup_logging()
    driver = setup_driver()
    grupos = load_messages()
    
    schedule.every(2).hours.do(procesar_envios, driver=driver, grupos=grupos)
    logging.info("🤖 Bot iniciado")
    procesar_envios(driver, grupos, con_delay=False)

    while True:
        try:
            schedule.run_pending()
            time.sleep(10)
        except KeyboardInterrupt:
            logging.info("\nPrograma detenido manualmente. ¡Adiós!")
            break
        except Exception as e:
            logging.error(f"Error inesperado en el bucle principal: {e}")
            break
    
    driver.quit()

if __name__ == "__main__":
    main()