import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

entrada_ativa = None
ultimo_processado = None

gale = 0
MAX_GALE = 1

historico = []

wins = 0
losses = 0
total = 0

ultimo_relatorio = 0

# 🔥 CONTROLE DE RECUPERAÇÃO
ultima_acao = time.time()

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

enviar("🚀 BOT INICIADO")

while True:

    # 🔥 AUTO-RECUPERAÇÃO (DESTRAVA O BOT)
    if time.time() - ultima_acao > 120:
        enviar("🔄 BOT DESINCRONIZADO — RESET AUTOMÁTICO")

        entrada_ativa = None
        gale = 0
        ultimo_processado = None

        ultima_acao = time.time()

    game_id, resultado = pegar_dados()

    if not game_id or not resultado:
        time.sleep(1)
        continue

    if game_id == ultimo_processado:
        time.sleep(1)
        continue

    ultimo_processado = game_id
    historico.append(resultado)

    print("RESULTADO:", resultado)

    # 🔥 atualiza ação
    ultima_acao = time.time()

    # =========================
    # PROCESSAR ENTRADA
    # =========================

    if entrada_ativa:

        if resultado == "T":
            enviar("⚖️ TIE")

        elif resultado == entrada_ativa:

            atualizar_stats(True)

            enviar("✅ WIN")

            entrada_ativa = None
            gale = 0

            ultima_acao = time.time()

        else:

            if gale < MAX_GALE:
                gale += 1
                enviar(f"⚠️ GALE {gale}")

                ultima_acao = time.time()

            else:
                atualizar_stats(False)

                enviar("❌ LOSS")

                entrada_ativa = None
                gale = 0

                ultima_acao = time.time()

    # =========================
    # NOVA ENTRADA
    # =========================

    if entrada_ativa is None:

        entrada, score = analisar(historico)

        if entrada and score >= 2:

            entrada_ativa = entrada
            gale = 0

            enviar_entrada(entrada, score)

            ultima_acao = time.time()

    # =========================
    # RELATÓRIO (SEM REPETIR)
    # =========================

    if total > 0 and total % 10 == 0 and total != ultimo_relatorio:

        enviar(f"""
📊 RELATÓRIO

🏆 Wins: {wins}
❌ Losses: {losses}
📈 Winrate: {placar():.2f}%
""")

        ultimo_relatorio = total

        ultima_acao = time.time()

    time.sleep(1)
