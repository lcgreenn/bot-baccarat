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

        outcome = data["data"]["result"]["outcome"]

        if outcome == "Banker":
            return "B"
        elif outcome == "Player":
            return "P"
        elif outcome == "Tie":
            return "T"

    except:
        return None

# 🔥 ESTRATÉGIA MELHORADA (menos sinais)
def analisar(h):
    if len(h) < 6:
        return None

    # sequência forte (4 iguais)
    if h[-4:] == ["B","B","B","B"]:
        return ("PLAYER", "Reversão forte 4x")

    if h[-4:] == ["P","P","P","P"]:
        return ("BANKER", "Reversão forte 4x")

    # padrão alternado forte
    if h[-5:] == ["B","P","B","P","B"]:
        return ("P", "Alternância")

    return None

def enviar_entrada(entrada, estrategia):
    enviar(f"""
🚨 ENTRADA CONFIRMADA

🎯 Entrada: {entrada}
📊 Estratégia: {estrategia}
🛡️ Gale: 1

🔥 FOCO TOTAL
""")

def enviar_resultado(resultado):
    if resultado:
        enviar("✅ WIN")
    else:
        enviar("❌ LOSS")

# ------------------------

historico = []
ultimo = None

entrada_ativa = None
gale = 0

enviar("🚀 BOT VIP ONLINE")

while True:
    resultado = pegar_resultado()

    if resultado and resultado != ultimo:
        ultimo = resultado
        historico.append(resultado)

        print("RESULTADO:", resultado)

        # 🔥 SE TEM ENTRADA ATIVA
        if entrada_ativa:
            esperado = entrada_ativa

            if resultado == esperado:
                enviar_resultado(True)
                entrada_ativa = None
                gale = 0

            elif gale == 0:
                gale = 1
                enviar("⚠️ GALE 1")

            else:
                enviar_resultado(False)
                entrada_ativa = None
                gale = 0

        else:
            sinal = analisar(historico)

            if sinal:
                entrada_ativa = sinal[0][0]  # B ou P
                enviar_entrada(sinal[0], sinal[1])

    time.sleep(5)
