import requests
import time
import random

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

FORCAR_ENTRADA = True

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

        outcome = data["data"]["result"]["outcome"]

        if outcome == "Banker":
            return "B"
        elif outcome == "Player":
            return "P"
        elif outcome == "Tie":
            return "T"

    except:
        return None

# ------------------------

entrada_ativa = None
ultimo_resultado = None

def fazer_entrada():
    return random.choice(["B", "P"])

enviar("🚀 TESTE INICIADO")

while True:
    resultado = pegar_resultado()

    if resultado and resultado != ultimo_resultado:
        ultimo_resultado = resultado

        print("RESULTADO:", resultado)

        # 🔥 VERIFICA RESULTADO IMEDIATO
        if entrada_ativa:

            if resultado == "T":
                enviar("⚖️ TIE — sem perda")
                continue

            if resultado == entrada_ativa:
                enviar("✅ WIN")
            else:
                enviar("❌ LOSS")

            entrada_ativa = None

        # 🔥 CRIA NOVA ENTRADA
        if FORCAR_ENTRADA and not entrada_ativa:
            entrada_ativa = fazer_entrada()

            enviar(f"""
🎯 ENTRADA

👉 {entrada_ativa}
""")

    time.sleep(1)
