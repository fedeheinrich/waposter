from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, random, schedule, datetime, os, logging

# --- Configuración del Logging ---
# Ruta Absoluta del Script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(script_dir, "logs")
os.makedirs(log_dir, exist_ok=True) # Crea la carpeta 'logs' si no existe

log_file_path = os.path.join(log_dir, "waposter.log")

# Configura el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler() # Esto envía el log también a la consola
    ]
)
# ---------------------------------

# Ruta del Driver de Edge (Automatizado)
logging.info("Configurando el driver de Edge (WebDriver-Manager)...")
service = EdgeService(EdgeChromiumDriverManager().install())
# Ruta Absoluta del archivo JSON con los mensajes
messages_path = os.path.join(script_dir, "data", "messages.json")

# Configuración del navegador Edge (mantiene sesión)
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_argument(f"user-data-dir={os.path.join(script_dir, 'WhatsAppBotProfile')}") # 🟢 Guarda sesión en una carpeta local
options.add_experimental_option("detach", True)

try:
    driver = webdriver.Edge(service=service, options=options)
    driver.get("https://web.whatsapp.com/") 
    logging.info("📱 Por favor, escaneá el código QR con tu teléfono y luego presioná ENTER en esta consola para continuar...")
    input()
    logging.info("QR escaneado. Iniciando bot...")
except Exception as e:
    logging.error(f"Error al iniciar el driver o WhatsApp Web: {e}")
    exit()

# Cargo los mensajes a enviar desde un archivo JSON
try:
    with open(messages_path, "r", encoding="utf-8") as file:
        grupos = json.load(file)
    logging.info(f"Se cargaron {len(grupos)} grupos desde {messages_path}")
except FileNotFoundError:
    logging.error(f"ERROR CRÍTICO: No se encontró el archivo 'data/messages.json'. Asegúrate de que exista.")
    exit()
except Exception as e:
    logging.error(f"Error al leer el archivo JSON: {e}")
    exit()

def tarea_programada():
    logging.info("--- Iniciando Tarea Programada ---")
    delay_minutos = random.randint(0, 10) # 0 a 10 minutos
    if delay_minutos > 0:
        delay_segundos = delay_minutos * 60
        logging.info(f"Retraso aleatorio activado. Esperando {delay_minutos} minutos ({delay_segundos}s) antes de enviar.")
        time.sleep(delay_segundos)
    
    enviar_mensajes()

def enviar_mensajes():
    wait = WebDriverWait(driver, 20)
    total_grupos = len(grupos)
    for i, grupo in enumerate(grupos):
        grupo_nombre = grupo["grupo"]
        logging.info(f"\n--- Procesando Grupo {i+1}/{total_grupos}: {grupo_nombre} ---")
        try:
            # 1. Busco el grupo en WhatsApp Web
            logging.info(f"Buscando grupo '{grupo_nombre}'...")
            # CORREGIDO: Selector XPATH más robusto
            buscar_grupo = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@role="textbox"][@title="Buscar contacto o chat"]')
            ))
            buscar_grupo.clear()
            buscar_grupo.send_keys(grupo_nombre)

            # 2. Espero a que el grupo aparezca en los resultados y le hago clic
            chat_grupo = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f'//span[@title="{grupo_nombre}"]')
            ))
            chat_grupo.click()
            logging.info(f"Grupo '{grupo_nombre}' encontrado y seleccionado.")

            # 3. Envío todos los mensajes definidos para el grupo
            total_mensajes = len(grupo["mensajes"])
            for j, mensaje in enumerate(grupo["mensajes"]):
                logging.info(f"Enviando mensaje {j+1}/{total_mensajes} a '{grupo_nombre}'...")
                try:
                    # Abrir boton de adjuntar
                    # CORREGIDO: Selector XPATH más robusto
                    boton_adjuntar = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@role="button"][@aria-label="Adjuntar"]')
                    ))
                    boton_adjuntar.click()

                    # Subir la imagen
                    # Este selector es bastante estable, se mantiene
                    input_archivo = wait.until(EC.presence_of_element_located(
                        (By.XPATH,'//input[@accept="image/*,video/*"]')
                    ))
                    
                    ruta_abs_imagen = os.path.join(script_dir, mensaje["imagen"])
                    if not os.path.exists(ruta_abs_imagen):
                        logging.warning(f"  Aviso: No se encontró la imagen en {ruta_abs_imagen}. Saltando este mensaje.")
                        continue

                    logging.info(f"  Adjuntando imagen: {mensaje['imagen']}")
                    input_archivo.send_keys(ruta_abs_imagen)

                    # 6. Escribir la descripcion (esperamos a que aparezca el cuadro de texto)
                    logging.info(f"  Escribiendo texto: {mensaje['texto'][:30]}...")
                    # CORREGIDO: Selector XPATH más robusto
                    descripcion = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@role="textbox"][@aria-label="Añade un comentario..."]')
                    ))
                    descripcion.send_keys(mensaje["texto"])
                    time.sleep(random.randint(1,5)) # Pausa "humana"

                   # 7. Enviar
                    # CORREGIDO: Selector XPATH más robusto
                    boton_enviar = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@role="button"][@aria-label="Enviar"]')
                    ))
                    boton_enviar.click()
                    logging.info(f"  ¡Mensaje enviado exitosamente!")

                    # Pausa larga entre mensajes para evitar spam
                    pausa_msg = random.randint(60,180)
                    logging.info(f"  Pausa 'anti-spam' de {pausa_msg} segundos...")
                    time.sleep(pausa_msg)
                
                except Exception as e:
                    logging.error(f"  ❌ Error al enviar un mensaje a {grupo_nombre}: {e}")
                    # Opcional: tomar un screenshot del error
                    driver.save_screenshot(f"error_mensaje_{grupo_nombre.replace(' ', '_')}.png")
                    logging.info("  Error capturado en screenshot. Intentando volver a la pantalla principal...")
                    driver.get("https://web.whatsapp.com/") # Volver a home para estabilizar
                    break # Salir del bucle de mensajes de este grupo

        except Exception as e:
            logging.error(f"❌❌ ERROR GRAVE: No se pudo procesar el grupo {grupo_nombre}. Saltando al siguiente.")
            logging.error(f"   Motivo: {e}")
            # Opcional: tomar un screenshot del error
            driver.save_screenshot(f"error_grupo_{grupo_nombre.replace(' ', '_')}.png")
            # Volver a la pantalla principal para buscar el siguiente grupo
            driver.get("https://web.whatsapp.com/")
            continue # Salta al siguiente GRUPO

    logging.info("\n🎉 ¡Todos los grupos procesados! Esperando la próxima ejecución programada.")


# --- EJECUCIÓN DE LA TAREA ---

schedule.every(2).hours.do(tarea_programada)

logging.info("🤖 Bot iniciado. Esperando para enviar mensajes cada 2 horas (Ctrl+C para detener)...")
while True:
    try:
        schedule.run_pending()
        time.sleep(10)
    except KeyboardInterrupt:
        logging.info("\nPrograma detenido manualmente. ¡Adiós!")
        driver.quit()
        break
    except Exception as e:
        logging.error(f"Error inesperado en el bucle principal: {e}")
        driver.quit()
        break