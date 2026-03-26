from downloader.ytdl import descargar

async def mp3(update, context):
    try:
        url = context.args[0]
        msg = await update.message.reply_text("🎵 Descargando MP3...")

        file = descargar(url, "mp3")

        await update.message.reply_audio(audio=open(file, "rb"))
        await msg.edit_text("✅ MP3 enviado")

    except:
        await update.message.reply_text("❌ Error en MP3")


async def mp4(update, context):
    try:
        url = context.args[0]
        msg = await update.message.reply_text("🎬 Descargando MP4...")

        file = descargar(url, "mp4")

        await update.message.reply_video(video=open(file, "rb"))
        await msg.edit_text("✅ MP4 enviado")

    except:
        await update.message.reply_text("❌ Error en MP4")