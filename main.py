import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

entrada_ativa = None
gale = 0
MAX_GALE = 1

historico = []

wins = 0
losses = 0
total = 0

ultimo_game = None

# 🔥 controle de travamento
ultimo_update = time.time()
TIMEOUT_RESET = 60  # segundos

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
    if len(h) < 4:
        return None, 0

    ultimos = h[-6:]

    score = 0
    entrada = None

    b = ultimos.count("B")
    p = ultimos.count("P")

    # 🔥 MAIS AGRESSIVO: tendência leve
    if b >= 4:
        score += 2
        entrada = "B"
    elif p >= 4:
        score += 2
        entrada = "P"

    # 🔥 REVERSÃO SIMPLES
    if ultimos[-3:] == ["B","B","B"]:
        score += 1
        entrada = "P"

    elif ultimos[-3:] == ["P","P","P"]:
        score += 1
        entrada = "B"
        
    # 🔥 TENDÊNCIA (forte)
    if b >= 6:
        score += 3
        entrada = "B"
    elif p >= 6:
        score += 3
        entrada = "P"

    # 🔥 TENDÊNCIA MÉDIA
    if b >= 5:
        score += 2
        entrada = "B"
    elif p >= 5:
        score += 2
        entrada = "P"

    # 🔥 REVERSÃO (padrão clássico)
    if ultimos[-4:] == ["B","B","B","B"]:
        score += 3
        entrada = "P"

    elif ultimos[-4:] == ["P","P","P","P"]:
        score += 3
        entrada = "B"

    # 🔥 ALTERNÂNCIA FORTE (ex: B P B P)
    alternancias = 0
    for i in range(len(ultimos)-1):
        if ultimos[i] != ultimos[i+1]:
            alternancias += 1

    if alternancias >= 6:
        score += 2
        entrada = None  # ⚠️ evita entrar em chop

    # 🔥 CHOP FILTER (mercado bagunçado)
    if alternancias >= 7:
        return None, 0  # ❌ não entra

    # 🔥 SURF (tendência limpa)
    if (b >= 7 and alternancias <= 3) or (p >= 7 and alternancias <= 3):
        score += 2

    # 🔥 CONFIRMAÇÃO DE CONTINUIDADE
    if len(ultimos) >= 3 and ultimos[-1] == ultimos[-2] == ultimos[-3]:
        score += 1

    return entrada, score

# ------------------------

def atualizar_stats(win):
    global wins, losses, total

    total += 1

    if win:
        wins += 1
    else:
        losses += 1

# ------------------------

def winrate():
    if total == 0:
        return 0
    return (wins / total) * 100

# ------------------------

enviar("🚀 BOT INICIADO (BLINDADO)")

while True:

    game_id, resultado = pegar_dados()

    if not game_id:
        time.sleep(1)
        continue

    # 🔥 SINCRONIZAÇÃO
    if game_id == ultimo_game:
        time.sleep(1)
        continue

    ultimo_game = game_id
    ultimo_update = time.time()

    # 🔥 RESET AUTOMÁTICO SE TRAVAR
    if time.time() - ultimo_update > TIMEOUT_RESET:
        enviar("♻️ RESET AUTOMÁTICO (DESINCRONIZADO)")
        entrada_ativa = None
        gale = 0
        historico.clear()

    # 🔥 TIE (NEUTRO)
    if resultado == "T":
        enviar("⚖️ TIE")
        continue

    historico.append(resultado)

    print("RESULTADO:", resultado)

    # =========================
    # PROCESSAMENTO
    # =========================

    if entrada_ativa:

        if resultado == entrada_ativa:

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

        if entrada and score >= 2:

            entrada_ativa = entrada
            gale = 0

            enviar(f"""
🚨 ENTRADA

🎯 {entrada}
📊 Score: {score}/10
""")

    # =========================
    # RELATÓRIO (SEM REPETIÇÃO)
    # =========================

    if total > 0 and total % 10 == 0:
        enviar(f"""
📊 RELATÓRIO

🏆 Wins: {wins}
❌ Losses: {losses}
📈 Winrate: {winrate():.2f}%
""")

    time.sleep(1)
