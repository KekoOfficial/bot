import asyncio
import re
import os
import glob

TEMP_PATH = "/data/data/com.termux/files/home/temp/"

os.makedirs(TEMP_PATH, exist_ok=True)

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

        match = re.search(r'(\d{1,3}\.\d+)%', text)
        if match:
            await progress_callback(match.group(1))

    await process.wait()

# 🎬 MP4
async def descargar_mp4(link, progress_callback):
    output = TEMP_PATH + "%(title)s.%(ext)s"

    cmd = f'''
    yt-dlp \
    -N 32 \
    --concurrent-fragments 32 \
    --downloader aria2c \
    --downloader-args "aria2c:-x 32 -s 32 -k 1M" \
    -f "bestvideo[height<=1080]+bestaudio/best" \
    --merge-output-format mp4 \
    --no-playlist \
    --newline \
    -o "{output}" "{link}"
    '''

    await run_cmd(cmd, progress_callback)

    files = glob.glob(TEMP_PATH + "*.mp4")
    return max(files, key=os.path.getctime)


# 🎵 MP3
async def descargar_mp3(link, progress_callback):
    output = TEMP_PATH + "%(title)s.%(ext)s"

    cmd = f'''
    yt-dlp \
    -x --audio-format mp3 \
    --no-playlist \
    --newline \
    -o "{output}" "{link}"
    '''

    await run_cmd(cmd, progress_callback)

    files = glob.glob(TEMP_PATH + "*.mp3")
    return max(files, key=os.path.getctime)