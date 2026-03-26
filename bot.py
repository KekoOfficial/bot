from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

from config import TOKEN
from downloader import descargar_mp3, descargar_mp4
from queue_system import add_to_queue, worker, queue

# 💀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💀 KHASAM BOT SYSTEM\n\n"
        "Comandos:\n"
        "/mp3 <link>\n"
        "/mp4 <link>\n\n"
        "⚡ Descarga FLASH + Cola inteligente"
    )

# 🎬 MP4
async def mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usa: /mp4 <link>")
        return

    link = context.args[0]
    pos = queue.qsize() + 1

    msg = await update.message.reply_text(f"🎬 En cola: #{pos}")

    async def job():
        last = "0"

        async def progress(p):
            nonlocal last
            if p != last:
                last = p
                try:
                    await msg.edit_text(f"🎬 Descargando MP4\n⚡ {p}%")
                except:
                    pass

        try:
            await descargar_mp4(link, progress)
            await msg.edit_text("✅ MP4 listo 🚀")
        except Exception as e:
            await msg.edit_text(f"❌ Error: {e}")

    await add_to_queue(job)

# 🎵 MP3
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usa: /mp3 <link>")
        return

    link = context.args[0]
    pos = queue.qsize() + 1

    msg = await update.message.reply_text(f"🎧 En cola: #{pos}")

    async def job():
        last = "0"

        async def progress(p):
            nonlocal last
            if p != last:
                last = p
                try:
                    await msg.edit_text(f"🎧 Descargando MP3\n⚡ {p}%")
                except:
                    pass

        try:
            await descargar_mp3(link, progress)
            await msg.edit_text("✅ MP3 listo 🚀")
        except Exception as e:
            await msg.edit_text(f"❌ Error: {e}")

    await add_to_queue(job)

# 🚀 MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", mp3))
    app.add_handler(CommandHandler("mp4", mp4))

    # 🔥 worker en segundo plano
    loop = asyncio.get_event_loop()
    loop.create_task(worker())

    print("💀 BOT ACTIVO FLASH...")
    app.run_polling()

if __name__ == "__main__":
    main()