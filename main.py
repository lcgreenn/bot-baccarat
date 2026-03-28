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
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, "html.parser")

        resultados = []

        for item in soup.find_all("div"):
            txt = item.text.strip()
            if txt in ["B", "P", "TIE"]:
                resultados.append(txt)

        print("RESULTADOS:", resultados)

        return resultados[-10:]

    except:
        return []

def analisar(h):
    if len(h) < 5:
        return None

    if h[-3:] == ["B","B","B"]:
        return ("PLAYER", "Reversão")

    if h[-3:] == ["P","P","P"]:
        return ("BANKER", "Reversão")

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

def status(msg):
    enviar(f"⚙️ STATUS: {msg}")

historico_antigo = []

status("BOT INICIADO")

while True:
    h = pegar_resultados()

    if not h:
        status("Sem dados do site")
        time.sleep(30)
        continue

    if h != historico_antigo:
        historico_antigo = h

        sinal = analisar(h)

        if sinal:
            enviar_sinal(sinal[0], sinal[1])

    time.sleep(10)
