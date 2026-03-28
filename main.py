import requests
import time
import random

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

entrada_ativa = None
ultimo_id = None

def enviar(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except:
        pass

def pegar_dados():
    try:
        r = requests.get(URL, timeout=10)
        data = r.json()

        game_id = data["data"]["id"]
        outcome = data["data"]["result"]["outcome"]

        if outcome == "Banker":
            return game_id, "B"
        elif outcome == "Player":
            return game_id, "P"
        elif outcome == "Tie":
            return game_id, "T"

    except:
        return None, None

def nova_entrada():
    return random.choice(["B", "P"])

enviar("🚀 BOT INICIADO")

while True:
    game_id, resultado = pegar_dados()

    if game_id and game_id != ultimo_id:
        ultimo_id = game_id

        print("RESULTADO:", resultado)

        # 🔥 VERIFICA RESULTADO
        if entrada_ativa:

            if resultado == "T":
                enviar("⚖️ TIE — sem perda")
                entrada_ativa = None
                continue

            if resultado == entrada_ativa:
                enviar("✅ WIN")
            else:
                enviar("❌ LOSS")

            entrada_ativa = None

        # 🔥 FAZ NOVA ENTRADA
        if not entrada_ativa:
            entrada_ativa = nova_entrada()

            enviar(f"""
🎯 ENTRADA

👉 {entrada_ativa}
""")

    time.sleep(1)
