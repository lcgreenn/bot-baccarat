import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://gamblingcounting.com/evolution-speed-baccarat-a/"

def enviar(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def pegar_resultados():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=headers, timeout=10)

        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []

        for div in soup.find_all("div"):
            classes = " ".join(div.get("class", []))

            if "red" in classes:
                resultados.append("B")
            elif "blue" in classes:
                resultados.append("P")
            elif "green" in classes:
                resultados.append("T")

        if len(resultados) < 5:
            return None

        return resultados[-20:]

    except:
        return None

def analisar(h):
    if len(h) < 5:
        return None

    if h[-3:] == ["B","B","B"]:
        return ("PLAYER", "Reversão 3x")

    if h[-3:] == ["P","P","P"]:
        return ("BANKER", "Reversão 3x")

    if h[-4:] == ["B","P","B","P"]:
        return ("BANKER", "Continuidade")

    return None

def enviar_sinal(entrada, estrategia):
    enviar(f"""
🚨 ENTRADA CONFIRMADA

🎯 Entrada: {entrada}
📊 Estratégia: {estrategia}
🛡️ Gale 1

🔥 FOCO
""")

historico = []
falhas = 0

enviar("🚀 BOT VIP ONLINE")

while True:
    dados = pegar_resultados()

    if dados is None:
        falhas += 1
        print("Falha ao puxar")

        if falhas >= 5:
            enviar("⚠️ Site instável, tentando reconectar...")
            falhas = 0

        time.sleep(25)
        continue

    falhas = 0

    if dados != historico:
        historico = dados

        sinal = analisar(dados)
        if sinal:
            enviar_sinal(sinal[0], sinal[1])

    time.sleep(20)
