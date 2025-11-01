# 📱 WAPOSTER 1.0 - Publicador de WhatsApp

<div align="center">

![WAPOSTER Logo](https://img.shields.io/badge/WAPOSTER-1.0-brightgreen.svg)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow.svg)
[![Estado](https://img.shields.io/badge/Estado-Activo-success.svg)](https://github.com/fedeheinrich/waposter)

</div>

## 🌟 Características Principales

- ✨ Envío automatizado de mensajes por WhatsApp
- 📸 Soporte para envío de imágenes
- 🔄 Sistema de plantillas personalizable
- 📋 Gestión de listas de destinatarios
- 📊 Seguimiento de envíos y reportes
- 🔒 Manejo seguro de credenciales

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
   python -m venv venv
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
├── data/
│   └── messages.json    # Configuración de mensajes
├── images/             # Imágenes de productos
│   ├── producto1.jpg
│   ├── producto2.jpg
│   └── producto3.jpg
└── README.md           # Documentación
```

### Configuración de Mensajes
El archivo `data/messages.json` debe seguir esta estructura:
```json
{
  "mensajes": [
    {
      "texto": "¡Oferta especial!",
      "imagen": "producto1.jpg",
      "destinatarios": ["+549XXXXXXXXXX"],
      "programado": "2025-11-01 15:00:00"
    }
  ]
}
```

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:
```env
```

## 🎯 Uso

1. **Preparación de Mensajes**:
   - Edita `data/messages.json` con tus mensajes
   - Coloca las imágenes en la carpeta `images/`
   - Verifica los números de destinatarios

2. **Ejecución**:
   ```bash
   python main.py
   ```

3. **Monitoreo**:
   - Revisa la consola para el estado de los envíos
   - Los logs se guardan en `logs/waposter.log`

## 🔍 Resolución de Problemas

### Errores Comunes
- **Error de Conexión**: Verifica tu conexión a Internet
- **Archivo no encontrado**: Asegúrate de que las imágenes existen en `images/`
- **Error de Autenticación**: Revisa tus credenciales en `.env`

### Logs
Los logs se encuentran en `logs/waposter.log` con detalles de cada operación.

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
