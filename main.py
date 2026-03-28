import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://gamblingcounting.com/evolution-speed-baccarat-a/"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def pegar_resultados():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        resultados = []

        # pega os círculos pelos estilos/classes
        for div in soup.find_all("div"):
            classes = str(div.get("class"))

            if "red" in classes:
                resultados.append("B")
            elif "blue" in classes:
                resultados.append("P")
            elif "green" in classes:
                resultados.append("T")

        print("RESULTADOS:", resultados)

        return resultados[-15:]

    except Exception as e:
        print("ERRO:", e)
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
    msg = f"""
🚨 ENTRADA CONFIRMADA

🎯 Entrada: {entrada}
📊 Estratégia: {estrategia}
🛡️ Proteção: Gale 1

🔥 FOCO TOTAL
"""
    enviar(msg)

historico_antigo = []

enviar("⚙️ BOT LENDO CORES (DADOS REAIS)")

while True:
    h = pegar_resultados()

    if not h:
        time.sleep(20)
        continue

    if h != historico_antigo:
        historico_antigo = h

        sinal = analisar(h)

        if sinal:
            enviar_sinal(sinal[0], sinal[1])

    time.sleep(15)
