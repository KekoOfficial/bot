import yt_dlp

def descargar(url, formato="mp3"):
    ydl_opts = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,

        # 🚀 velocidad máxima
        "concurrent_fragment_downloads": 10,

        "external_downloader": "aria2c",
        "external_downloader_args": [
            "-x", "10",  # 10 conexiones
            "-k", "1M"
        ],
    }

    if formato == "mp3":
        ydl_opts.update({
            "format": "bestaudio",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })

    elif formato == "mp4":
        ydl_opts.update({
            "format": "bestvideo+bestaudio/best",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)