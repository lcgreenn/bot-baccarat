import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

def enviar(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except:
        pass

def pegar_resultado():
    try:
        r = requests.get(URL, timeout=10)
        data = r.json()

        # tenta pegar outcome
        outcome = data.get("outcome")

        if outcome:
            if "banker" in outcome.lower():
                return "B"
            elif "player" in outcome.lower():
                return "P"
            elif "tie" in outcome.lower():
                return "T"

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
ultimo = None

enviar("🚀 BOT API ONLINE (DADOS REAIS)")

while True:
    resultado = pegar_resultado()

    if resultado and resultado != ultimo:
        ultimo = resultado
        historico.append(resultado)

        print("NOVO RESULTADO:", resultado)

        sinal = analisar(historico)
        if sinal:
            enviar_sinal(sinal[0], sinal[1])

    time.sleep(5)
