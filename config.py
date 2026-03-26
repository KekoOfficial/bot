# config.py
# ⚡ Configuración principal del KHASAM BOT

# TOKEN de tu bot en Telegram
TOKEN = "8783635581:AAEEAqLo8kAair708D8E23g_mH10oiIriGo"  # Reemplaza con el token real de tu bot

# Carpeta temporal (no guarda permanentemente archivos)
TEMP_PATH = "/data/data/com.termux/files/home/temp/"

# Formatos y opciones predeterminadas
VIDEO_FORMAT = "bestvideo[height<=1080]+bestaudio/best"
AUDIO_FORMAT = "mp3"

# Descarga rápida / ultra flash
YTDLP_THREADS = 32  # Número de fragmentos concurrentes
ARIA2_ARGS = "-x 32 -s 32 -k 1M"

# Geo bypass para plataformas bloqueadas
GEO_BYPASS = True

# Límite de tamaño recomendado para enviar por Telegram
TELEGRAM_LIMIT_MB = 50