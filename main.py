import requests
import time
import random

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

# ------------------------

entrada_ativa = None
ultimo_id = None
ultimo_processado = None

gale = 0
MAX_GALE = 1

historico = []

wins = 0
losses = 0
total = 0

# ------------------------

def enviar(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except:
        pass

# ------------------------

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

# ------------------------

def analisar(h):
    if len(h) < 10:
        return None, 0

    score = 0
    entrada = None

    # 🔥 TENDÊNCIA LONGA (mais forte)
    if h[-5:] == ["B","B","B","B","B"]:
        score += 5
        entrada = "P"

    elif h[-5:] == ["P","P","P","P","P"]:
        score += 5
        entrada = "B"

    # 🔥 TENDÊNCIA MÉDIA (com confirmação)
    elif h[-4:] == ["B","B","B","B"]:
        score += 3
        entrada = "P"

    elif h[-4:] == ["P","P","P","P"]:
        score += 3
        entrada = "B"

    # 🔥 CONFIRMAÇÃO DE CONTINUIDADE
    if h[-3:] == ["B","B","B"]:
        score += 2

    if h[-3:] == ["P","P","P"]:
        score += 2

    # 🔥 FILTRO CHOP FORTE (EVITA LIXO)
    if h[-6:] == ["B","P","B","P","B","P"]:
        return None, 0

    if h[-6:] == ["P","B","P","B","P","B"]:
        return None, 0

    # 🔥 FILTRO DE ALEATORIEDADE
    ultimos = h[-6:]
    if ultimos.count("B") == 3 and ultimos.count("P") == 3:
        return None, 0

    # 🔥 REGRA FINAL DE QUALIDADE
    if score < 7:
        return None, score

    return entrada, score

# ------------------------

def enviar_entrada(entrada, score):
    enviar(f"""
🚨 ENTRADA

🎯 {entrada}
📊 Score: {score}/10
🛡️ Gale: {MAX_GALE}
""")

# ------------------------

def atualizar_stats(win):
    global wins, losses, total

    total += 1

    if win:
        wins += 1
    else:
        losses += 1

def placar():
    if total == 0:
        return 0
    return (wins / total) * 100

# ------------------------

enviar("🚀 BOT CORRIGIDO INICIADO")

while True:

    game_id, resultado = pegar_dados()

    if not game_id or not resultado:
        time.sleep(1)
        continue

    # 🔒 evita processar o mesmo resultado
    if game_id == ultimo_processado:
        time.sleep(1)
        continue

    ultimo_processado = game_id

    historico.append(resultado)

    print("RESULTADO:", resultado)

    # =========================
    # 🔥 PROCESSAR ENTRADA ATIVA
    # =========================

    if entrada_ativa:

        if resultado == "T":
            enviar("⚖️ TIE — sem perda")

        elif resultado == entrada_ativa:

            atualizar_stats(True)

            enviar("✅ WIN")

            entrada_ativa = None
            gale = 0

        else:

            if gale < MAX_GALE:
                gale += 1
                enviar(f"⚠️ GALE {gale}")

            else:
                atualizar_stats(False)

                enviar("❌ LOSS FINAL")

                entrada_ativa = None
                gale = 0

    # =========================
    # 🔥 NOVA ENTRADA
    # =========================

    if entrada_ativa is None:

        entrada, score = analisar(historico)

        if entrada and score >= 6:

            entrada_ativa = entrada
            gale = 0

            enviar_entrada(entrada, score)

    # =========================
    # 📊 RELATÓRIO
    # =========================

    if total > 0 and total % 10 == 0:
        enviar(f"""
📊 RELATÓRIO

🏆 Wins: {wins}
❌ Loss: {losses}
📈 Winrate: {placar():.2f}%
""")

    time.sleep(1)
