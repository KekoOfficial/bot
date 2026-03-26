import os
import asyncio
from config import DOWNLOAD_PATH

async def descargar_mp4(link):
    cmd = f'''
    yt-dlp \
    -N 16 \
    --concurrent-fragments 16 \
    --downloader aria2c \
    --downloader-args "aria2c:-x 16 -s 16 -k 1M" \
    -f "bestvideo[height<=1080][vcodec*=avc1]+bestaudio[acodec*=mp4a]/best[height<=1080]" \
    --merge-output-format mp4 \
    --recode-video mp4 \
    --fragment-retries 100 \
    --retries 20 \
    -o "{DOWNLOAD_PATH}%(title)s.mp4" "{link}"
    '''
    os.system(cmd)

async def descargar_mp3(link):
    cmd = f'''
    yt-dlp \
    -x --audio-format mp3 \
    -o "{DOWNLOAD_PATH}%(title)s.mp3" "{link}"
    '''
    os.system(cmd)