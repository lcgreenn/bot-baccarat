import requests
import time
import random

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

# ------------------------

entrada_ativa = None
ultimo_id = None

gale = 0
MAX_GALE = 1

historico = []

# 📊 ESTATÍSTICAS
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
# 🧠 SCORE PROFISSIONAL

def analisar(h):
    if len(h) < 8:
        return None, 0

    score = 0
    entrada = None

    # 🔥 TENDÊNCIA FORTE
    if h[-3:] == ["B","B","B"]:
        score += 3
        entrada = "B"

    elif h[-3:] == ["P","P","P"]:
        score += 3
        entrada = "P"

    # 🔥 REVERSÃO
    if h[-4:] == ["B","B","B","B"]:
        score += 4
        entrada = "P"

    elif h[-4:] == ["P","P","P","P"]:
        score += 4
        entrada = "B"

    # 🔥 CONFIRMAÇÃO
    if h[-2:] == ["B","B"]:
        score += 1

    if h[-2:] == ["P","P"]:
        score += 1

    # 🔥 FILTRO DE CHOP (MUITO IMPORTANTE)
    if h[-6:] == ["B","P","B","P","B","P"]:
        return None, 0

    # 🔥 CONFLUÊNCIA DE FORÇA
    if h[-5:].count("B") >= 4:
        score += 2
        entrada = "B"

    if h[-5:].count("P") >= 4:
        score += 2
        entrada = "P"

    return entrada, score

# ------------------------

def enviar_entrada(entrada, score):
    enviar(f"""
🚨 ENTRADA CONFIRMADA

🎯 Entrada: {entrada}
📊 Score: {score}/10

🛡️ Gale: {MAX_GALE}

🔥 Sistema ativo
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

enviar("🚀 BOT PROFISSIONAL INICIADO")

while True:

    game_id, resultado = pegar_dados()

    if game_id and game_id != ultimo_id:

        ultimo_id = game_id
        historico.append(resultado)

        print("RESULTADO:", resultado)

        # 🔥 RESULTADO DA ENTRADA
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

        # 🔥 NOVA ANÁLISE
        entrada, score = analisar(historico)

        # 🔥 REGRA PROFISSIONAL DE ENTRADA
        if entrada and score >= 2 and not entrada_ativa:

            entrada_ativa = entrada
            gale = 0

            enviar_entrada(entrada_ativa, score)

        # 🔥 RELATÓRIO PERIÓDICO
        if total > 0 and total % 10 == 0:
            enviar(f"""
📊 RELATÓRIO

🏆 Wins: {wins}
❌ Loss: {losses}
📈 Winrate: {placar():.2f}%
""")

    time.sleep(1)
