# bot.py v3
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from downloader import download_stream
from config import BOT_TOKEN, MESSAGES, DOWNLOAD_QUEUE, MAX_CONCURRENT_DOWNLOADS, add_to_queue, pop_from_queue

current_downloads = 0

# -------------------
# Comandos
# -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MESSAGES["start"])

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /mp3 o /mp4
    """
    global current_downloads
    if not context.args:
        await update.message.reply_text("❌ Envía un enlace después del comando, ej: /mp4 https://...")
        return

    url = context.args[0]
    file_type = update.message.text[1:]  # mp3 o mp4
    add_to_queue((url, file_type, update))
    await update.message.reply_text(f"⚡ Encolado: {url}")
    await process_queue()

# -------------------
# Cola de descargas
# -------------------
async def process_queue():
    """
    Procesa la cola hasta el máximo de descargas simultáneas
    """
    global current_downloads
    while current_downloads < MAX_CONCURRENT_DOWNLOADS and DOWNLOAD_QUEUE:
        url, file_type, update = pop_from_queue()
        current_downloads += 1
        asyncio.create_task(send_download(update, url, file_type))

async def send_download(update: Update, url: str, file_type: str):
    """
    Descarga y envía a Telegram sin guardar en disco
    """
    global current_downloads
    try:
        msg = await update.message.reply_text("⏳ Preparando descarga...")

        # Callback de progreso
        async def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '0.0%').strip()
                await msg.edit_text(f"⚡ Descargando {file_type}...\nProgreso: {percent}")

        # Descargar y enviar en memoria
        await download_stream(url, file_type, progress_callback=progress_hook, chat_id=update.effective_chat.id, bot=update.bot)
        await msg.edit_text(f"✅ Descarga {file_type.upper()} completa y enviada")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
    finally:
        current_downloads -= 1
        await process_queue()  # Procesar siguiente en cola

# -------------------
# Inicialización
# -------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["mp3","mp4"], download_command))

    print("💀 BOT ACTIVO STREAM ULTRA FLASH...")
    app.run_polling(drop_pending_updates=True)