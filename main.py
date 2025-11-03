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

# --- SELECTORES XPATH ACTUALIZADOS ---
XPATHS = {
    "buscar_chat": '//input[@placeholder="Buscar un chat o iniciar uno nuevo"]',  # Alternativa 1
    "buscar_chat_alt1": '//input[contains(@placeholder, "Buscar")]',  # Alternativa 2
    "buscar_chat_alt2": '//div[@contenteditable="true"][@data-tab="0"]',  # Alternativa 3
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

def escribir_en_campo_busqueda(driver, texto):
    """
    Escribe en el campo de búsqueda carácter por carácter 
    para que WhatsApp detecte cada pulsación.
    """
    try:
        # Encontrar el campo contenteditable
        campos = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')
        
        if not campos:
            logging.error("   ✗ No se encontró el campo contenteditable")
            return False
        
        campo = campos[0]
        
        # Hacer clic en el campo para enfocarlo
        campo.click()
        time.sleep(0.3)
        
        # Limpiar con Ctrl+A y Delete
        campo.send_keys(Keys.CONTROL + "a")
        time.sleep(0.1)
        campo.send_keys(Keys.DELETE)
        time.sleep(0.2)
        
        # Escribir carácter por carácter para simular escritura humana
        logging.info(f"   Escribiendo: {texto}")
        for i, char in enumerate(texto):
            campo.send_keys(char)
            # Pequeña pausa entre caracteres para simular escritura real
            if i % 5 == 0:  # Pausa cada 5 caracteres
                time.sleep(random.uniform(0.05, 0.1))
        
        time.sleep(0.3)
        logging.info(f"   ✓ Texto escrito: '{texto}'")
        return True
        
    except Exception as e:
        logging.error(f"   ✗ Error al escribir en el campo: {e}")
        return False

def hacer_clic_en_primer_resultado(driver):
    """
    Espera a que aparezcan resultados y hace clic en el primero.
    """
    try:
        max_intentos = 5
        for intento in range(max_intentos):
            # Buscar elementos de resultado
            resultados = driver.find_elements(By.XPATH, '//div[@role="option"]')
            
            if resultados:
                logging.info(f"   ✓ Encontrados {len(resultados)} resultado(s)")
                resultados[0].click()
                logging.info(f"   ✓ Se hizo clic en el primer resultado")
                time.sleep(1.5)
                return True
            
            if intento < max_intentos - 1:
                logging.info(f"   Esperando resultados... ({intento + 1}/{max_intentos})")
                time.sleep(0.5)
        
        logging.warning(f"   ⚠ No se encontraron resultados después de esperar")
        return False
        
    except Exception as e:
        logging.error(f"   Error al hacer clic: {e}")
        return False

def buscar_y_abrir_grupo(driver, wait, grupo_nombre):
    """
    Busca un grupo y lo abre usando Selenium con escritura carácter por carácter.
    """
    try:
        logging.info(f"Procesando grupo: '{grupo_nombre}'")
        
        # 1. Encontrar el campo de búsqueda
        logging.info("   Encontrando campo de búsqueda...")
        campos = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')
        
        if not campos:
            logging.error("   ✗ No se encontró el campo de búsqueda")
            return False
        
        campo = campos[0]
        logging.info("   ✓ Campo encontrado")
        
        # 2. Escribir en el campo
        if not escribir_en_campo_busqueda(driver, grupo_nombre):
            return False
        
        time.sleep(3)  # Esperar a que WhatsApp procese la búsqueda
        
        # 3. Hacer clic en el primer resultado
        logging.info("   Buscando resultados...")
        if hacer_clic_en_primer_resultado(driver):
            logging.info(f"✅ ¡Grupo abierto exitosamente!")
            time.sleep(1)
            return True
        else:
            logging.error(f"❌ No se encontraron resultados para '{grupo_nombre}'")
            return False
    
    except Exception as e:
        logging.error(f"❌ Error inesperado: {repr(e)}")
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
            time.sleep(2)  # ← AGREGAR ESTA PAUSA
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
        
        # ← AGREGAR ESTA PAUSA AL FINAL DE CADA GRUPO
        if i < total_grupos - 1:  # No pausar después del último grupo
            pausa_grupo = random.randint(2, 5)
            logging.info(f"Pausa entre grupos: {pausa_grupo} segundos...")
            time.sleep(pausa_grupo)
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