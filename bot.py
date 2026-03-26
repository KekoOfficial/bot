from telegram.ext import ApplicationBuilder, CommandHandler
from config import TOKEN
from handlers.media import mp3, mp4

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("mp3", mp3))
app.add_handler(CommandHandler("mp4", mp4))

print("🔥 BOT KHASAM ACTIVO")
app.run_polling()