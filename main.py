import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

# ------------------------

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
# 🔥 ANÁLISE MELHORADA

def analisar(h):
    if len(h) < 8:
        return None

    # reversão forte
    if h[-5:] == ["B","B","B","B","B"]:
        return ("P", "Reversão 5x")

    if h[-5:] == ["P","P","P","P","P"]:
        return ("B", "Reversão 5x")

    # alternância
    if h[-6:] == ["B","P","B","P","B","P"]:
        return ("B", "Alternância longa")

    if h[-6:] == ["P","B","P","B","P","B"]:
        return ("P", "Alternância longa")

    # tendência
    if h[-3:] == ["B","B","B"]:
        return ("B", "Trend 3x")

    if h[-3:] == ["P","P","P"]:
        return ("P", "Trend 3x")

    # quebra
    if h[-4:] == ["B","B","P","B"]:
        return ("P", "Quebra")

    if h[-4:] == ["P","P","B","P"]:
        return ("B", "Quebra")

    # filtro anti-surf simples
    if len(h) >= 10:
        b = h[-10:].count("B")
        p = h[-10:].count("P")
        if abs(b - p) < 2:
            return None

    return None

# ------------------------

def enviar_entrada(entrada, estrategia):
    enviar(f"""
🚨 ENTRADA

🎯 {entrada}
📊 {estrategia}
🛡️ Gale: 1
""")

def enviar_resultado(win):
    if win:
        enviar("✅ WIN")
    else:
        enviar("❌ LOSS")

# ------------------------

historico = []
ultimo = None

entrada_ativa = None
gale = 0

enviar("🚀 BOT ONLINE")

while True:
    resultado = pegar_resultado()

    if resultado and resultado != ultimo:
        ultimo = resultado
        historico.append(resultado)

        print("RESULTADO:", resultado)

        # ------------------------
        # 🔥 SE EXISTE ENTRADA ATIVA
        if entrada_ativa:
            esperado = entrada_ativa["lado"]

            if resultado == esperado:
                enviar_resultado(True)
                entrada_ativa = None
                gale = 0

            else:
                # gale 1
                if gale == 0:
                    gale = 1
                    enviar("⚠️ GALE 1")

                # gale 2
                else:
                    enviar_resultado(False)
                    entrada_ativa = None
                    gale = 0

        # ------------------------
        # 🔥 SE NÃO TEM ENTRADA ATIVA
        else:
            sinal = analisar(historico)

            if sinal:
                entrada_ativa = {
                    "lado": sinal[0],
                    "estrategia": sinal[1]
                }

                enviar_entrada(sinal[0], sinal[1])

    time.sleep(2)  # ⏱️ mais rápido pra teste
