import requests
import time
import random

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

historico = []

def gerar_resultado():
    return random.choice(["P", "B"])  # Player / Banker

def analisar(h):
    if len(h) < 5:
        return None

    # Reversão
    if h[-3:] == ["B","B","B"]:
        return ("PLAYER", "Reversão")

    if h[-3:] == ["P","P","P"]:
        return ("BANKER", "Reversão")

    # Alternância
    if h[-4:] == ["B","P","B","P"]:
        return ("BANKER", "Continuidade")

    return None

def enviar_sinal(entrada, estrategia):
    msg = f"""
🚨 ENTRADA CONFIRMADA

🎯 Entrada: {entrada}
📊 Estratégia: {estrategia}
🛡️ Proteção: Gale 1

🔥 FOCO TOTAL
"""
    enviar(msg)

while True:
    resultado = gerar_resultado()
    historico.append(resultado)

    sinal = analisar(historico)

    if sinal:
        enviar_sinal(sinal[0], sinal[1])
        time.sleep(60)

    time.sleep(10)
