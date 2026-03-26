# config.py
# 💀 KHASAM BOT CONFIG - v2.0

import os

# -----------------------------
# 🔹 TOKEN DEL BOT
# -----------------------------
# Reemplaza con tu token real de BotFather
BOT_TOKEN = "8783635581:AAEEAqLo8kAair708D8E23g_mH10oiIriGo"

# -----------------------------
# 🔹 PATH DE DESCARGA
# -----------------------------
# Carpeta temporal donde se guardan los archivos antes de enviarlos
# Si quieres que no se guarden, deja como None
TEMP_DOWNLOAD_PATH = None  # o "/sdcard/Download" para guardar temporalmente

# -----------------------------
# 🔹 OPCIONES DE DESCARGA
# -----------------------------
# Formato de salida por defecto
DEFAULT_FORMATS = {
    "mp4": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "mp3": "bestaudio/best"
}

# Fragmentos concurrentes (velocidad máxima)
FRAGMENTS = 16

# Número de reintentos por fragmento
FRAGMENT_RETRIES = 100

# Número total de reintentos por descarga
TOTAL_RETRIES = 20

# Downloader externo (aria2c recomendado para ultra velocidad)
DOWNLOADER = "aria2c"
DOWNLOADER_ARGS = "-x 16 -s 16 -k 1M"

# -----------------------------
# 🔹 COLA DE DESCARGA
# -----------------------------
# Limitar descargas simultáneas
MAX_CONCURRENT_DOWNLOADS = 2  # Cambiar según RAM/dispositivo

# Lista temporal de URLs en cola
DOWNLOAD_QUEUE = []

# -----------------------------
# 🔹 MENSAJES DEL BOT
# -----------------------------
MESSAGES = {
    "start": "💀 KHASAM BOT ACTIVADO\n\nEnvía un link:\n🎵 MP3\n🎬 MP4\n\n⚡ Sistema modular activo",
    "download_start": "⚡ Descargando tu archivo... Esto puede tardar unos segundos",
    "download_progress": "📊 Progreso: {progress}%",
    "download_complete": "✅ Descarga lista, enviando ahora...",
    "error": "❌ Ocurrió un error en la descarga o el enlace es inválido"
}

# -----------------------------
# 🔹 LOGGING / DEBUG
# -----------------------------
DEBUG = True  # True = muestra logs detallados, False = logs mínimos

# -----------------------------
# 🔹 UTILIDADES
# -----------------------------
def add_to_queue(url: str):
    """Agrega un link a la cola de descargas"""
    DOWNLOAD_QUEUE.append(url)

def pop_from_queue():
    """Saca el primer link de la cola"""
    if DOWNLOAD_QUEUE:
        return DOWNLOAD_QUEUE.pop(0)
    return None

# -----------------------------
# 🔹 OTROS AJUSTES
# -----------------------------
# Evitar guardar archivos en disco si TEMP_DOWNLOAD_PATH = None
STREAM_DIRECTLY = True