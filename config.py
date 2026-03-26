# config.py
BOT_TOKEN = "8783635581:AAEEAqLo8kAair708D8E23g_mH10oiIriGo"

MESSAGES = {
    "start": "💀 KHASAM BOT ULTRA FLASH\n\nEnvía un link:\n🎵 /mp3\n🎬 /mp4\n\n⚡ Cola y descarga ultra rápida activa"
}

DOWNLOAD_QUEUE = []
MAX_CONCURRENT_DOWNLOADS = 2  # Ajusta según tu conexión

def add_to_queue(item):
    DOWNLOAD_QUEUE.append(item)

def pop_from_queue():
    return DOWNLOAD_QUEUE.pop(0)