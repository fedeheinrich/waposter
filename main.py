from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, random, schedule, datetime, os

# Ruta Absoluta del Script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ruta del Driver de Edge
service = Service("msedgedriver")
# Ruta Absoluta del archivo JSON con los mensajes
messages_path = os.path.join(script_dir, "messages.json")

# Configuración del navegador Edge (mantiene sesión)
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_argument(f"user-data-dir={os.path.join(script_dir, 'WhatsAppBotProfile')}") # 🟢 Guarda sesión en una carpeta local
options.add_experimental_option("detach", True)
driver = webdriver.Edge(service=service, options=options)

driver.get("https://web.whatsapp.com/") 
print("📱 Escaneá el código QR con tu teléfono y luego presioná ENTER para continuar...")
input()

# Cargo los mensajes a enviar desde un archivo JSON
with open(messages_path, "r", encoding="utf-8") as file:
    grupos = json.load(file)

def tarea_programada():
    delay = random.randint(-10, 10) * 60
    if delay > 0:
        time.sleep(delay)
    enviar_mensajes()

def enviar_mensajes():
    wait = WebDriverWait(driver, 20)
    for grupo in grupos:
        try:
            # 1. Busco el grupo en WhatsApp Web
            buscar_grupo = wait.until(EC.element_to_be_clickable(
                (By.XPATH,'//div[@contenteditable="true"][@data-tab="3"]')
            ))
            buscar_grupo.clear()
            buscar_grupo.send_keys(grupo["grupo"])

            # 2. Espero a que el grupo aparezca en los resultados y le hago clic
            chat_grupo = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f'//span[@title="{grupo["grupo"]}"]')
            ))
            chat_grupo.click()

            # 3. Envío todos los mensajes definidos para el grupo
            for mensaje in grupo["mensajes"]:
                try:
                    # Abrir boton de adjuntar
                    boton_adjuntar = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,'//div[@title="Adjuntar"]')
                    ))
                    boton_adjuntar.click()

                    # Subir la imagen
                    input_archivo = wait.until(EC.presence_of_element_located(
                        (By.XPATH,'//input[@accept="image/*,video/*"]')
                    ))
                    # ¡Mejora clave! Construimos la ruta absoluta de la imagen
                    ruta_abs_imagen = os.path.join(script_dir, mensaje["imagen"])
                    input_archivo.send_keys(ruta_abs_imagen)

                    # 6. Escribir la descripcion (esperamos a que aparezca el cuadro de texto)
                    descripcion = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,'//div[@contenteditable="true"][@data-tab="10"]')
                    ))
                    descripcion.send_keys(mensaje["texto"])
                    time.sleep(random.randint(1,5)) # Pausa "humana"

                   # 7. Enviar
                    boton_enviar = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,'//span[@data-icon="send"]')
                    ))
                    boton_enviar.click()

                    # Pausa larga entre mensajes para evitar spam
                    pausa_msg = random.randint(60,180)
                    time.sleep(pausa_msg)
                except Exception as e:
                    print(f"  ❌ Error al enviar un mensaje a {grupo['grupo']}: {e}")
                    # Opcional: tomar un screenshot del error
                    driver.save_screenshot(f"error_mensaje_{grupo['grupo']}.png")
                    continue # Salta al siguiente MENSAJE

        except Exception as e:
            print(f"❌❌ ERROR GRAVE: No se pudo procesar el grupo {grupo['grupo']}. Saltando al siguiente.")
            print(f"   Motivo: {e}")
            # Opcional: tomar un screenshot del error
            driver.save_screenshot(f"error_grupo_{grupo['grupo']}.png")
            # Volver a la pantalla principal para buscar el siguiente grupo
            driver.get("https://web.whatsapp.com/")
            continue # Salta al siguiente GRUPO

    print("\n🎉 ¡Todos los grupos procesados! Esperando la próxima ejecución programada.")


# --- EJECUCIÓN DE LA TAREA ---

schedule.every(2).hours.do(tarea_programada)

print("🤖 Bot iniciado. Esperando para enviar mensajes cada 2 horas...")
while True:
    schedule.run_pending()
    time.sleep(10)


