import subprocess
import time
import os

# 🔹 Matar procesos previos del bot
os.system("pkill -f bot.py")

# 🔹 Esperar unos segundos para que se cierre la sesión
time.sleep(3)

# 🔹 Ejecutar bot.py
subprocess.run(["python", "bot.py"])