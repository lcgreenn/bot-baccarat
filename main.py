import requests
import time
import random

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

# 🔥 MODO TESTE FORÇADO
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

    except:
        return None

# ------------------------

entrada_ativa = None
ultimo = None

def fazer_entrada():
    lado = random.choice(["B", "P"])
    return lado

enviar("🚀 TESTE DE ENTRADAS ATIVO")

while True:
    resultado = pegar_resultado()

    if resultado and resultado != ultimo:
        ultimo = resultado

        print("RESULTADO:", resultado)

        # 🔥 SE NÃO TEM ENTRADA ATIVA → FAZ UMA
        if FORCAR_ENTRADA and not entrada_ativa:
            entrada_ativa = fazer_entrada()

            enviar(f"""
🎯 ENTRADA FORÇADA

👉 {entrada_ativa}
""")

        # 🔥 SE TEM ENTRADA → VERIFICA RESULTADO
        elif entrada_ativa:
            if resultado == entrada_ativa:
                enviar("✅ WIN")
            else:
                enviar("❌ LOSS")

            entrada_ativa = None

    time.sleep(2)
