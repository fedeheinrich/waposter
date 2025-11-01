# 📱 WAPOSTER 1.0 - Publicador de WhatsApp

<div align="center">

![WAPOSTER Logo](https://img.shields.io/badge/WAPOSTER-1.0-brightgreen.svg)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow.svg)
[![Estado](https://img.shields.io/badge/Estado-Activo-success.svg)](https://github.com/fedeheinrich/waposter)

</div>

## 🌟 Características Principales

- ✨ **Envío Automatizado**: Programa y envía mensajes a múltiples grupos de WhatsApp sin intervención manual.
- 📸 **Soporte Multimedia**: Envía mensajes que incluyen texto e imágenes.
- 🔄 **Programación Flexible**: Configurado para ejecutarse cada 2 horas, con un retraso aleatorio para simular comportamiento humano.
- 📂 **Sesión Persistente**: Guarda la sesión de WhatsApp para no tener que escanear el código QR en cada ejecución.
- 🪵 **Logging Detallado**: Registra cada acción en `logs/waposter.log`, facilitando el seguimiento y la depuración.
- 🛡️ **Manejo de Errores Robusto**: Detecta errores durante el envío, guarda una captura de pantalla y continúa con el siguiente grupo.

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta activa de WhatsApp
- Conexión estable a Internet
- Paquetes Python listados en `requirements.txt`

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/fedeheinrich/waposter.git
   cd waposter
   ```

2. Crea y activa un entorno virtual:
   ```bash
   py -m venv env
   # En Windows
   .\venv\Scripts\activate
   # En Linux/Mac
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuración

### Estructura del Proyecto
```
waposter/
├── main.py              # Script principal
├── requirements.txt     # Dependencias
├── msedgedriver.exe    # Driver de Microsoft Edge
├── data/
│   └── messages.json    # Configuración de mensajes
├── images/             # Imágenes de productos
│   ├── producto1.jpg
│   ├── producto2.jpg
│   └── producto3.jpg
├── logs/               # Directorio de registros
└── README.md           # Documentación
```

### Configuración de Mensajes
El archivo `data/messages.json` debe seguir esta estructura:
```json
[
    {
        "grupo": "Nombre del Grupo 1",
        "mensajes": [
            {
                "texto": "Mensaje de Producto 1",
                "imagen": "images/producto1.jpg"
            },
            {
                "texto": "Mensaje de Producto 2",
                "imagen": "images/producto2.jpg"
            },
            {
                "texto": "Mensaje de Producto 3",
                "imagen": "images/producto3.jpg"
            }
        ]
    },
    {
        "grupo": "Nombre del Grupo 2",
        "mensajes": [
            {
                "texto": "Mensaje de Producto 1",
                "imagen": "images/producto1.jpg"
            },
            {
                "texto": "Mensaje de Producto 2",
                "imagen": "images/producto2.jpg"
            },
            {
                "texto": "Mensaje de Producto ...",
                "imagen": "images/producto3.jpg"
            }
        ]
    },
]
```

## 🎯 Uso

1.  **Configuración**:
    *   Abre el archivo `data/messages.json` y define los grupos de destino y los mensajes que deseas enviar.
    *   Asegúrate de que las imágenes referenciadas en el JSON existan en la carpeta `images/`.

2.  **Ejecución Inicial**:
    *   Ejecuta el script desde tu terminal:
        ```bash
        python main.py
        ```
    *   La primera vez, se abrirá WhatsApp Web. Deberás **escanear el código QR** con tu teléfono.
    *   Una vez escaneado, presiona `ENTER` en la terminal. La sesión se guardará en la carpeta `WhatsAppBotProfile` para futuros inicios.

3.  **Monitoreo**:
    *   El bot comenzará su ciclo de envío programado. Puedes ver el progreso en tiempo real en la consola.
    *   Para un análisis más detallado, revisa el archivo `logs/waposter.log`.
    *   Para detener el bot de forma segura, presiona `Ctrl+C` en la terminal.

## ⚠️ Uso Responsable

El uso de herramientas de automatización en WhatsApp va en contra de sus Términos de Servicio y puede resultar en el **bloqueo temporal o permanente de tu número**. Para minimizar los riesgos, este script incluye pausas y retrasos aleatorios.

- **No abuses del sistema**: Evita enviar mensajes masivos en cortos períodos de tiempo.
- **Contenido Relevante**: Asegúrate de que los mensajes sean relevantes y esperados por los miembros del grupo.
- **Usa bajo tu propio riesgo**: El desarrollador no se hace responsable por el bloqueo de cuentas o cualquier otra consecuencia derivada del mal uso de esta herramienta.

## 🔍 Resolución de Problemas

### Errores Comunes
- **Error al iniciar el driver**: Asegúrate de tener Microsoft Edge instalado. `WebDriver-Manager` se encargará del resto.
- **El grupo no se encuentra**: Verifica que el nombre del grupo en `messages.json` coincida **exactamente** con el nombre en WhatsApp.
- **Archivo de imagen no encontrado**: Comprueba que la ruta en `messages.json` (ej: `images/producto1.jpg`) sea correcta y que el archivo exista.

### Logs y Capturas de Pantalla
- **Logs**: Todos los eventos, advertencias y errores se guardan en `logs/waposter.log`. Es el primer lugar que debes revisar si algo falla.
- **Capturas de Error**: Si ocurre un error grave durante el procesamiento de un grupo o mensaje, el script guardará una captura de pantalla (ej: `error_grupo_...png`) en la carpeta principal del proyecto. Estas imágenes son muy útiles para entender qué falló en la interfaz de WhatsApp.

## 🤝 Contribuciones

1. Haz un Fork del proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Federico Heinrich** - *Desarrollo Inicial* - [fedeheinrich](https://github.com/fedeheinrich)

## 🙋‍♂️ Soporte

¿Tienes preguntas o necesitas ayuda?
- Abre un issue en GitHub

## 🌟 Agradecimientos

- A la comunidad de Python
- A todos los contribuidores
- A los usuarios que confían en WAPOSTER

---

<div align="center">
Hecho con ❤️ por Federico Heinrich
</div>
