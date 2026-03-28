import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://gamblingcounting.com/evolution-speed-baccarat-a/"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def pegar_resultados():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(URL, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        resultados = []

        # pega os círculos (onde ficam B, P, T)
        for span in soup.find_all("span"):
            txt = span.text.strip()

            if txt == "B":
                resultados.append("B")
            elif txt == "P":
                resultados.append("P")
            elif txt == "T":
                resultados.append("T")

        print("RESULTADOS:", resultados)

        return resultados[-15:]

    except Exception as e:
        print("ERRO:", e)
        return []

def analisar(h):
    if len(h) < 5:
        return None

    # Reversão forte
    if h[-3:] == ["B","B","B"]:
        return ("PLAYER", "Reversão 3x")

    if h[-3:] == ["P","P","P"]:
        return ("BANKER", "Reversão 3x")

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

def status(msg):
    enviar(f"⚙️ STATUS: {msg}")

historico_antigo = []

status("BOT ONLINE (DADOS REAIS)")

while True:
    h = pegar_resultados()

    if not h:
        status("Erro ao puxar dados")
        time.sleep(30)
        continue

    if h != historico_antigo:
        historico_antigo = h

        sinal = analisar(h)

        if sinal:
            enviar_sinal(sinal[0], sinal[1])

    time.sleep(10)
