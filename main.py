import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://www.casino.org/casinoscores/pt-br/speed-baccarat-a/"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def pegar_resultados():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    resultados = []

    # tenta pegar os blocos B / P / TIE
    for item in soup.find_all("div"):
        txt = item.text.strip()
        if txt in ["B", "P", "TIE"]:
            resultados.append(txt)

    return resultados[-10:]  # últimos 10

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

historico_antigo = []

while True:
    try:
        h = pegar_resultados()

        if h != historico_antigo:
            historico_antigo = h

            sinal = analisar(h)

            if sinal:
                enviar_sinal(sinal[0], sinal[1])

        time.sleep(10)

    except:
        time.sleep(15)
