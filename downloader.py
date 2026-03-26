import asyncio
import re
import os
import glob
from config import TEMP_PATH, VIDEO_FORMAT, AUDIO_FORMAT, YTDLP_THREADS, ARIA2_ARGS, GEO_BYPASS

# Crear carpeta temporal si no existe
os.makedirs(TEMP_PATH, exist_ok=True)

# Ejecutar comando yt-dlp con progreso
async def run_cmd(cmd, progress_callback):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        text = line.decode("utf-8", errors="ignore")

        # Buscar porcentaje de progreso
        match = re.search(r'(\d{1,3}\.\d+)%', text)
        if match:
            await progress_callback(match.group(1))

    await process.wait()
    return process.returncode

# Descarga MP4 (video)
async def descargar_mp4(link, progress_callback):
    output = TEMP_PATH + "%(title)s.%(ext)s"
    geo = "--geo-bypass" if GEO_BYPASS else ""
    cmd = f'''
    yt-dlp -N {YTDLP_THREADS} \
    --concurrent-fragments {YTDLP_THREADS} \
    --downloader aria2c \
    --downloader-args "aria2c:{ARIA2_ARGS}" \
    -f "{VIDEO_FORMAT}" {geo} \
    --merge-output-format mp4 \
    --no-playlist \
    --newline \
    -o "{output}" "{link}"
    '''
    await run_cmd(cmd, progress_callback)

    files = glob.glob(TEMP_PATH + "*.mp4")
    if not files:
        raise Exception("❌ No se pudo descargar el video. Link inválido o protegido.")
    return max(files, key=os.path.getctime)

# Descarga MP3 (audio)
async def descargar_mp3(link, progress_callback):
    output = TEMP_PATH + "%(title)s.%(ext)s"
    geo = "--geo-bypass" if GEO_BYPASS else ""
    cmd = f'''
    yt-dlp -x --audio-format {AUDIO_FORMAT} \
    -N {YTDLP_THREADS} \
    --no-playlist \
    --newline \
    {geo} \
    -o "{output}" "{link}"
    '''
    await run_cmd(cmd, progress_callback)

    files = glob.glob(TEMP_PATH + "*.mp3")
    if not files:
        raise Exception("❌ No se pudo descargar el audio. Link inválido o protegido.")
    return max(files, key=os.path.getctime)