import asyncio
import re

# 🚀 Ejecutar comando y capturar progreso
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

        # 🔥 detectar %
        match = re.search(r'(\d{1,3}\.\d+)%', text)
        if match:
            await progress_callback(match.group(1))

    await process.wait()


# 🎬 MP4 FLASH SPEED
async def descargar_mp4(link, progress_callback):
    cmd = f'''
    yt-dlp \
    -N 32 \
    --concurrent-fragments 32 \
    --downloader aria2c \
    --downloader-args "aria2c:-x 32 -s 32 -k 1M" \
    -f "bestvideo[height<=1080][vcodec*=avc1]+bestaudio[acodec*=mp4a]/best[height<=1080]" \
    --merge-output-format mp4 \
    --recode-video mp4 \
    --no-playlist \
    --newline \
    "{link}"
    '''
    await run_cmd(cmd, progress_callback)


# 🎵 MP3 FLASH SPEED
async def descargar_mp3(link, progress_callback):
    cmd = f'''
    yt-dlp \
    -x --audio-format mp3 \
    -N 16 \
    --no-playlist \
    --newline \
    "{link}"
    '''
    await run_cmd(cmd, progress_callback)