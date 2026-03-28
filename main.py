import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

entrada_ativa = None
ultimo_game = None

gale = 0
MAX_GALE = 1

historico = []

wins = 0
losses = 0
total = 0

# 🔥 CONTROLE DE LOOP / ESTABILIDADE
ultimo_envio_entrada = 0
ultimo_relatorio = 0

# ------------------------

def enviar(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
    except Exception as e:
        print("Erro envio:", e)

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

# 🔥 SCORE PROFISSIONAL
def analisar(h):
    if len(h) < 10:
        return None, 0

    ult = h[-10:]

    score = 0
    entrada = None

    b = ult.count("B")
    p = ult.count("P")

    # 🔥 TENDÊNCIA FORTE
    if b >= 7:
        score += 4
        entrada = "B"
    elif p >= 7:
        score += 4
        entrada = "P"

    # 🔥 TENDÊNCIA MÉDIA
    elif b >= 5:
        score += 2
        entrada = "B"
    elif p >= 5:
        score += 2
        entrada = "P"

    # 🔥 REVERSÃO
    if ult[-4:] == ["B","B","B","B"]:
        score += 3
        entrada = "P"

    elif ult[-4:] == ["P","P","P","P"]:
        score += 3
        entrada = "B"

    # 🔥 CHOP FILTER (anti bagunça)
    alternancias = 0
    for i in range(len(ult)-1):
        if ult[i] != ult[i+1]:
            alternancias += 1

    if alternancias >= 7:
        return None, 0

    # 🔥 CONFIRMAÇÃO DE PADRÃO
    if len(ult) >= 3 and ult[-1] == ult[-2] == ult[-3]:
        score += 1

    # 🔥 FILTRO FINAL
    if score < 3:
        return None, score

    return entrada, score

# ------------------------

def enviar_entrada(entrada, score):
    global ultimo_envio_entrada

    # evita spam
    if time.time() - ultimo_envio_entrada < 20:
        return

    ultimo_envio_entrada = time.time()

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

# ------------------------

def placar():
    if total == 0:
        return 0
    return (wins / total) * 100

# ------------------------

enviar("🚀 BOT INICIADO")

while True:

    game_id, resultado = pegar_dados()

    if not game_id or not resultado:
        time.sleep(1)
        continue

    if game_id == ultimo_game:
        time.sleep(1)
        continue

    ultimo_game = game_id

    historico.append(resultado)

    print("RESULTADO:", resultado)

    # =========================
    # GERENCIAMENTO DA ENTRADA
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

        if entrada:

            entrada_ativa = entrada
            gale = 0

            enviar_entrada(entrada, score)

    # =========================
    # RELATÓRIO
    # =========================

    if total > 0 and total % 10 == 0 and total != ultimo_relatorio:

        enviar(f"""
📊 RELATÓRIO

🏆 Wins: {wins}
❌ Losses: {losses}
📈 Winrate: {placar():.2f}%
""")

        ultimo_relatorio = total

    time.sleep(1)
