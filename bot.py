from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

from config import TOKEN
from downloader import descargar_mp3, descargar_mp4
from queue_system import add_to_queue, worker, queue

# 🔥 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💀 KHASAM BOT SYSTEM\n\n"
        "Usa:\n"
        "/mp3 <link>\n"
        "/mp4 <link>\n\n"
        "⚡ Cola inteligente activa"
    )

# 🎵 MP3
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = context.args[0]

    pos = queue.qsize() + 1

    await update.message.reply_text(f"🎧 Añadido a cola: #{pos}")

    async def job():
        await update.message.reply_text("⬇️ Descargando MP3...")
        await descargar_mp3(link)
        await update.message.reply_text("✅ MP3 listo")

    await add_to_queue(job)

# 🎬 MP4
async def mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = context.args[0]

    pos = queue.qsize() + 1

    await update.message.reply_text(f"🎬 Añadido a cola: #{pos}")

    async def job():
        await update.message.reply_text("⬇️ Descargando MP4 1080p...")
        await descargar_mp4(link)
        await update.message.reply_text("✅ MP4 listo")

    await add_to_queue(job)

# 🚀 MAIN
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", mp3))
    app.add_handler(CommandHandler("mp4", mp4))

    # worker en segundo plano
    asyncio.create_task(worker())

    print("💀 BOT ACTIVO...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())