from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

from config import TOKEN, TEMP_PATH
from downloader import descargar_mp3, descargar_mp4

# Cola de descargas
queue = asyncio.Queue()

async def add_to_queue(job):
    await queue.put(job)

async def worker():
    while True:
        job = await queue.get()
        try:
            await job()
        except Exception as e:
            print("❌ Error en job:", e)
        queue.task_done()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💀 KHASAM BOT SYSTEM\n\n"
        "Comandos:\n"
        "/mp3 <link>\n/mp4 <link>\n\n"
        "⚡ Descarga ultra rápida + envío directo"
    )

# Comando /mp4
async def mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usa: /mp4 <link>")
        return
    link = context.args[0]
    msg = await update.message.reply_text("🎬 En cola...")

    async def job():
        last = "0"
        async def progress(p):
            nonlocal last
            if p != last:
                last = p
                try:
                    await msg.edit_text(f"🎬 Descargando...\n⚡ {p}%")
                except:
                    pass
        try:
            file_path = await descargar_mp4(link, progress)
            await msg.edit_text("📤 Enviando video...")
            with open(file_path, "rb") as f:
                await update.message.reply_video(f)
            os.remove(file_path)
            await msg.edit_text("✅ Video enviado 🚀")
        except Exception as e:
            await msg.edit_text(f"❌ {e}")

    await add_to_queue(job)

# Comando /mp3
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usa: /mp3 <link>")
        return
    link = context.args[0]
    msg = await update.message.reply_text("🎧 En cola...")

    async def job():
        last = "0"
        async def progress(p):
            nonlocal last
            if p != last:
                last = p
                try:
                    await msg.edit_text(f"🎧 Descargando...\n⚡ {p}%")
                except:
                    pass
        try:
            file_path = await descargar_mp3(link, progress)
            await msg.edit_text("📤 Enviando audio...")
            with open(file_path, "rb") as f:
                await update.message.reply_audio(f)
            os.remove(file_path)
            await msg.edit_text("✅ Audio enviado 🚀")
        except Exception as e:
            await msg.edit_text(f"❌ {e}")

    await add_to_queue(job)

# MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", mp3))
    app.add_handler(CommandHandler("mp4", mp4))

    loop = asyncio.get_event_loop()
    loop.create_task(worker())

    print("💀 BOT ACTIVO STREAM...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()