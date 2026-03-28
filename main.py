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

# 🔥 NOVA VARIÁVEL (EVITA REPETIÇÃO DO RELATÓRIO)
ultimo_relatorio = 0

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

# 🔥 ESTRATÉGIA
def analisar(h):
    if len(h) < 6:
        return None

    if h[-4:] == ["B","B","B","B"]:
        return ("PLAYER", "Reversão forte 4x")

    if h[-4:] == ["P","P","P","P"]:
        return ("BANKER", "Reversão forte 4x")

    if h[-5:] == ["B","P","B","P","B"]:
        return ("P", "Alternância")

    return None

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

if not inicio_enviado:
    enviar("🚀 BOT INICIADO")
    inicio_enviado = True

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

            enviar_entrada(entrada, score)

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

    time.sleep(1)
