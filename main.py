import requests
import time
import random

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

# 🔥 MODO TESTE (simulação)
MODO_TESTE = False

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
        if MODO_TESTE:
            return random.choice(["B","P"])

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
# 🔥 MÉTODOS (MAIS SINAIS)

def analisar(h):
    if len(h) < 6:
        return None

    # reversão longa
    if h[-5:] == ["B","B","B","B","B"]:
        return ("P", "Reversão 5x")

    if h[-5:] == ["P","P","P","P","P"]:
        return ("B", "Reversão 5x")

    # reversão média
    if h[-4:] == ["B","B","B","B"]:
        return ("P", "Reversão 4x")

    if h[-4:] == ["P","P","P","P"]:
        return ("B", "Reversão 4x")

    # alternância
    if h[-4:] == ["B","P","B","P"]:
        return ("B", "Alternância")

    if h[-4:] == ["P","B","P","B"]:
        return ("P", "Alternância")

    # tendência curta
    if h[-3:] == ["B","B","B"]:
        return ("B", "Trend 3x")

    if h[-3:] == ["P","P","P"]:
        return ("P", "Trend 3x")

    # quebra de sequência
    if len(h) >= 5:
        if h[-3] == h[-4] and h[-1] != h[-2]:
            return ("P" if h[-1] == "B" else "B", "Quebra")

    # 🔥 filtro anti-surf
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

enviar("🚀 BOT EM TESTE")

# 🔥 modo teste rápido (opcional)
delay = 1 if MODO_TESTE else 2

while True:
    resultado = pegar_resultado()

    if resultado and resultado != ultimo:
        ultimo = resultado
        historico.append(resultado)

        print("RESULTADO:", resultado)

        # ------------------------
        # 🔥 SE TEM ENTRADA
        if entrada_ativa:
            esperado = entrada_ativa["lado"]

            if resultado == esperado:
                enviar_resultado(True)
                entrada_ativa = None
                gale = 0

            else:
                if gale == 0:
                    gale = 1
                    enviar("⚠️ GALE 1")
                else:
                    enviar_resultado(False)
                    entrada_ativa = None
                    gale = 0

        # ------------------------
        # 🔥 NOVA ENTRADA
        else:
            sinal = analisar(historico)

            if sinal:
                entrada_ativa = {
                    "lado": sinal[0],
                    "estrategia": sinal[1]
                }

                enviar_entrada(sinal[0], sinal[1])

    time.sleep(delay)
