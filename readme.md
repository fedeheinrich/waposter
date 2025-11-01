# Publicador WhatsApp - WAPOSTER 1.0

Pequeña utilidad para publicar y enviar mensajes e imágenes a través de WhatsApp desde scripts locales. Incluye un script principal `main.py`, un archivo de configuración de mensajes `data/messages.json` y una carpeta `images/` con productos.

## Estructura del proyecto

- `main.py` - Punto de entrada del programa.
- `requirements.txt` - Dependencias de Python.
- `data/messages.json` - Mensajes y plantillas a enviar.
- `images/` - Imágenes de productos utilizadas en los envíos.
- `readme.md` - Documentación del proyecto.

## Requisitos

- Python 3.8 o superior.
- Paquetes listados en `requirements.txt`.

## Instalación

1. Crear y activar un entorno virtual de Python.
2. Instalar dependencias desde `requirements.txt`.

## Configuración

- Edita `data/messages.json` para definir los mensajes que quieres enviar. Cada entrada debe incluir texto, destinatarios y la referencia a la imagen si procede.
- Coloca las imágenes en la carpeta `images/` con nombres que coincidan con las referencias en el JSON.
- Si el script requiere credenciales o tokens, almacénalos de forma segura (variables de entorno o un archivo `.env`) y no los subas al repositorio.

## Uso

- Ejecuta `main.py` para iniciar el proceso de publicación. El script leerá `data/messages.json` y enviará los mensajes e imágenes configuradas.
- Revisa la salida en consola para ver el estado de cada envío y posibles errores.

## Buenas prácticas

- Haz pruebas enviando mensajes a números de prueba antes de lanzar envíos masivos.
- Asegúrate de cumplir las políticas de WhatsApp y las leyes locales sobre envío de mensajes.

## Contribuciones

Pull requests y reportes de issues son bienvenidos. Describe claramente los cambios propuestos y provee ejemplos si es posible.

## Licencia

Incluye aquí la licencia del proyecto (por ejemplo, MIT) o la nota "Todos los derechos reservados" si aplica.
