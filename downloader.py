# downloader.py
import asyncio
import yt_dlp
from config import TEMP_DOWNLOAD_PATH, DEFAULT_FORMATS, FRAGMENTS, FRAGMENT_RETRIES, TOTAL_RETRIES, DOWNLOADER, DOWNLOADER_ARGS, STREAM_DIRECTLY

async def download(url: str, file_type: str, progress_callback=None):
    """
    Descarga un archivo usando yt-dlp y envía progreso.
    :param url: URL del video/audio
    :param file_type: 'mp3' o 'mp4'
    :param progress_callback: función async(progress_dict)
    """
    ydl_opts = {
        "format": DEFAULT_FORMATS[file_type],
        "noplaylist": True,
        "concurrent_fragment_downloads": FRAGMENTS,
        "fragment_retries": FRAGMENT_RETRIES,
        "retries": TOTAL_RETRIES,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [progress_callback] if progress_callback else [],
        "outtmpl": TEMP_DOWNLOAD_PATH or "%(title)s.%(ext)s",
        "postprocessors": [],
    }

    if file_type == "mp3":
        ydl_opts["postprocessors"].append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        })

    if STREAM_DIRECTLY:
        ydl_opts["outtmpl"] = "-"  # stream directo

    if DOWNLOADER:
        ydl_opts["external_downloader"] = DOWNLOADER
        ydl_opts["external_downloader_args"] = DOWNLOADER_ARGS.split()

    loop = asyncio.get_event_loop()
    # Ejecutar descarga en thread para no bloquear
    await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))