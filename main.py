from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, json, random, schedule, datetime

# Ruta del Driver de Edge
service = Service("msedgedriver")

# Configuración del navegador Edge (mantiene sesión)
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
options.add_argument("user-data-dir=C:/WhatsAppBotProfile")  # 🟢 Guarda sesión en esa carpeta
options.add_experimental_option("detach", True)
driver = webdriver.Edge(service=service, options=options)

driver.get("https://web.whatsapp.com/") 
print("📱 Escaneá el código QR con tu teléfono y luego presioná ENTER para continuar...")
input()

# Cargo los mensajes a enviar desde un archivo JSON
with open("messages.json", "r", encoding="utf-8") as file:
    grupos = json.load(file)

def enviar_mensajes():
    for grupo in grupos:
        # Busco el grupo en WhatsApp Web
        buscar_grupo = driver.find_element(By.XPATH,'//div[@contenteditable="true"][@data-tab="3"]')
        buscar_grupo.clear()
        buscar_grupo.send_keys(grupo["grupo"])
        time.sleep(2)
        buscar_grupo.send_keys(Keys.ENTER)
        time.sleep(2)

        # Envío todos los mensajes definidos para el grupo
        for mensaje in grupo["mensajes"]:
            # Abrir boton de adjuntar
            boton_adjuntar = driver.find_element(By.XPATH,'//div[@title="Adjuntar"]')
            boton_adjuntar.click()
            time.sleep(1)

            # Subir la imagen
            input_archivo = driver.find_element(By.XPATH,'//input[@accept="image/*,video/*"]')
            input_archivo.send_keys(mensaje["imagen"])
            time.sleep(2)

            # Escribir la descripcion
            descripcion = driver.find_element(By.XPATH,'//div[@contenteditable="true"][@data-tab="10"]')
            descripcion.send_keys(mensaje["texto"])
            time.sleep(random.randint(1,5))

            # Enviar
            boton_enviar = driver.find_element(By.XPATH,'//span[@data-icon="send"]')
            boton_enviar.click()
            time.sleep(random.randint(60,180)) # pequeña pausa entre mensajes



