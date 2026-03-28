import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def sinal_teste():
    msg = """
🚨 BOT ONLINE

✅ Sistema ativo
📡 Enviando sinais automático

🔥 Preparando análise...
"""
    enviar(msg)

while True:
    sinal_teste()
    time.sleep(60)
