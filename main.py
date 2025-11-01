from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, json, random, schedule

# Ruta del Driver de Edge
service = Service("msedgedriver")

# Configuración del navegador Edge
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized") # Abre la ventana maximizada
options.add_experimental_option("detach", True) # Mantiene la ventana abierta después de ejecutar el script
driver = webdriver.Edge(service=Service, options = options)


driver.get("https://web.whatsapp.com/") 
print("📱 Escaneá el código QR con tu teléfono y luego presioná ENTER para continuar...")
input()
# Cargo los mensajes a enviar desde un archivo JSON
with open("menssages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)

def enviar_mensajes():
    for message in messages:
        # Busco el grupo en WhatsApp Web
        buscar_grupo = driver.find_element(By.XPATH,'//div[@contenteditable="true"][@data-tab="3"]')
        buscar_grupo.clear()
        buscar_grupo.send_keys(message["grupo"])
        time.sleep(2)
        buscar_grupo.send_keys(Keys.ENTER)
        time.sleep(2)

        # Envío los mensajes al grupo
        




