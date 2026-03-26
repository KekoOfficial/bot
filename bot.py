# bot.py
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from downloader import download
from config import BOT_TOKEN, MESSAGES, DOWNLOAD_QUEUE, MAX_CONCURRENT_DOWNLOADS, add_to_queue, pop_from_queue

# Para manejar descargas simultáneas
current_downloads = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MESSAGES["start"])

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_downloads
    if not context.args:
        await update.message.reply_text("❌ Envía un enlace después del comando, ej: /mp4 https://...")
        return

    url = context.args[0]
    file_type = update.message.text[1:]  # mp3 o mp4
    add_to_queue((url, file_type, update))

    await update.message.reply_text(f"⚡ Encolado: {url}")

    # Procesar cola
    await process_queue()

async def process_queue():
    global current_downloads
    while current_downloads < MAX_CONCURRENT_DOWNLOADS and DOWNLOAD_QUEUE:
        url, file_type, update = pop_from_queue()
        current_downloads += 1
        await send_download(update, url, file_type)
        current_downloads -= 1

async def send_download(update: Update, url: str, file_type: str):
    try:
        msg = await update.message.reply_text(MESSAGES["download_start"])

        async def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '0.0%').strip()
                await msg.edit_text(MESSAGES["download_progress"].format(progress=percent))

        await download(url, file_type, progress_callback=progress_hook)
        await msg.edit_text(MESSAGES["download_complete"])
        # Enviar directo al chat (stream)
        # Si TEMP_DOWNLOAD_PATH=None, yt-dlp hace streaming
        # Aquí puedes usar context.bot.send_document si quieres enviar el archivo
    except Exception as e:
        await update.message.reply_text(f"{MESSAGES['error']}\n{e}")

# -------------------
# Inicialización del bot
# -------------------
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["mp3","mp4"], download_command))
    # Evitar conflicto con sesiones viejas
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.start()
    print("💀 BOT ACTIVO STREAM...")
    await app.updater.start_polling(drop_pending_updates=True)
    await app.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # Deprecation warning loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())