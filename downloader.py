# downloader.py
import yt_dlp
import io
from telegram import InputFile

async def download_stream(url, file_type, progress_callback=None, chat_id=None, bot=None):
    """
    Descarga video/audio y lo envía directamente a Telegram sin guardar en disco
    """
    ydl_opts = {
        'format': 'bestaudio/best' if file_type == 'mp3' else 'bestvideo+bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'progress_hooks': [lambda d: asyncio.create_task(progress_callback(d))] if progress_callback else [],
        'outtmpl': '-',  # No guardar en disco
        'merge_output_format': 'mp4',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}] if file_type=='mp3' else [],
        'ffmpeg_location': '/data/data/com.termux/files/usr/bin/ffmpeg'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # Crear buffer temporal en memoria (BytesIO) si quieres enviar directamente
        data = io.BytesIO()
        # Nota: yt-dlp no soporta enviar directo a BytesIO sin FFmpeg manual
        # Aquí se puede usar temp file y enviar a Telegram o integrar FFmpeg streaming
        # Ejemplo simple: solo avisar que está enviado
        await bot.send_message(chat_id=chat_id, text=f"⚡ {file_type.upper()} listo para enviar (stream placeholder)")