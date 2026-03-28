import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

# ------------------------

entrada_ativa = None
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
    if len(h) < 12:
        return None, 0

    ultimos = h[-10:]

    score = 0
    entrada = None

    b = ultimos.count("B")
    p = ultimos.count("P")

    # 🔥 TENDÊNCIA FORTE
    if b >= 7:
        score += 4
        entrada = "B"
    elif p >= 7:
        score += 4
        entrada = "P"

    # 🔥 REVERSÃO
    if ultimos[-4:] == ["B","B","B","B"]:
        score += 3
        entrada = "P"

    elif ultimos[-4:] == ["P","P","P","P"]:
        score += 3
        entrada = "B"

    # 🔥 CHOP FILTER
    alternancias = 0
    for i in range(len(ultimos)-1):
        if ultimos[i] != ultimos[i+1]:
            alternancias += 1

    if alternancias >= 7:
        return None, 0

    score += abs(b - p)

    return entrada, score

# ------------------------

def enviar_entrada(entrada, score):
    enviar(f"""
🚨 ENTRADA

🎯 Direção: {entrada}
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

enviar("🚀 BOT INICIADO")

# ------------------------
# LOOP PRINCIPAL
# ------------------------

while True:

    game_id, resultado = pegar_dados()

    if not game_id or not resultado:
        time.sleep(1)
        continue

    # evita duplicação
    if game_id == ultimo_processado:
        time.sleep(1)
        continue

    ultimo_processado = game_id

    print("RESULTADO:", resultado)

    # adiciona histórico
    historico.append(resultado)

    # =========================
    # RESULTADO DA ENTRADA
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
                enviar("❌ LOSS")

                entrada_ativa = None
                gale = 0

    # =========================
    # NOVA ENTRADA
    # =========================

    if entrada_ativa is None:

        entrada, score = analisar(historico)

        if entrada and score >= 7:

            entrada_ativa = entrada
            gale = 0

            enviar_entrada(entrada, score)

    # =========================
    # RELATÓRIO
    # =========================

    if total > 0 and total % 10 == 0:
        enviar(f"""
📊 RELATÓRIO

🏆 Wins: {wins}
❌ Loss: {losses}
📈 Winrate: {placar():.2f}%
""")

    time.sleep(1)
