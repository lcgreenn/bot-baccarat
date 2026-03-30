import requests
import time

TOKEN = "8781756079:AAF39To2Wh_v8IM1koM14nLQHDK-WTIyPJI"
CHAT_ID = "@lcgreenbaccarat"

URL = "https://api-cs.casino.org/svc-evolution-game-events/api/speedbaccarata/latest"

entrada_ativa = None
ultimo_game = None

historico = []

wins = 0
losses = 0
total = 0

ultimo_relatorio = 0

# 🔥 CONTROLE TELEGRAM
offset = None
rodando = True

# 🔥 ESTABILIDADE
ultimo_update = time.time()
TEMPO_LIMITE = 120
ja_resetou = False

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

def verificar_comandos():
    global offset, rodando

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        if offset:
            url += f"?offset={offset}"

        r = requests.get(url, timeout=10).json()

        for update in r["result"]:
            offset = update["update_id"] + 1

            if "message" in update:
                texto = update["message"].get("text", "")

                if texto == "/stop":
                    rodando = False
                    enviar("⛔ BOT PAUSADO")

                elif texto == "/start":
                    rodando = True
                    enviar("▶️ BOT ATIVADO")

                elif texto == "/status":
                    enviar(f"""
📊 STATUS

🏆 Wins: {wins}
❌ Losses: {losses}
📈 Winrate: {placar():.2f}%
""")
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
    if len(h) < 6:
        return None, 0

    ult = h[-8:]

    score = 0
    entrada = None

    b = ult.count("B")
    p = ult.count("P")

    if b >= 6:
        score += 3
        entrada = "B"
    elif p >= 6:
        score += 3
        entrada = "P"

    elif b >= 5:
        score += 2
        entrada = "B"
    elif p >= 5:
        score += 2
        entrada = "P"

    if ult[-4:] == ["B","B","B","B"]:
        score += 2
        entrada = "P"

    elif ult[-4:] == ["P","P","P","P"]:
        score += 2
        entrada = "B"

    if len(ult) >= 3 and ult[-1] == ult[-2]:
        score += 1

    alternancias = sum(1 for i in range(len(ult)-1) if ult[i] != ult[i+1])

    if alternancias >= 6:
        return None, 0

    if alternancias >= 4:
        score -= 1

    if score < 3:
        return None, score

    return entrada, score

# ------------------------

def enviar_entrada(entrada, score):
    enviar(f"""
🚨 ENTRADA

🎯 {entrada}
📊 Score: {score}/10
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

enviar("🚀 BOT INICIADO (TIE FIXADO)")

while True:

    verificar_comandos()

    if not rodando:
        time.sleep(1)
        continue

    agora = time.time()

    if agora - ultimo_update > TEMPO_LIMITE:
        if not ja_resetou:
            enviar("♻️ RE-SINCRONIZANDO...")
            entrada_ativa = None
            ja_resetou = True

        time.sleep(1)
        continue

    game_id, resultado = pegar_dados()

    if not game_id or not resultado:
        time.sleep(1)
        continue

    if game_id == ultimo_game:
        time.sleep(1)
        continue

    ultimo_game = game_id
    ultimo_update = time.time()
    ja_resetou = False

    print("RESULTADO:", resultado)

    # 🔥 SALVA SE HAVIA ENTRADA ANTES DO RESULTADO
    tinha_entrada = entrada_ativa is not None

    # =========================
    # 🔥 TIE CORRETO (SEM BUG)
    # =========================
    if resultado == "T":

        if tinha_entrada:
            enviar("⚖️ TIE")
            enviar("⚪️ ENTRADA CANCELADA (TIE)")
            entrada_ativa = None

        continue

    historico.append(resultado)

    # =========================
    # RESULTADO NORMAL
    # =========================

    if tinha_entrada:

        if resultado == entrada_ativa:
            atualizar_stats(True)
            enviar("✅ WIN")
        else:
            atualizar_stats(False)
            enviar("❌ LOSS")

        entrada_ativa = None

    # =========================
    # NOVA ENTRADA
    # =========================

    if entrada_ativa is None:

        entrada, score = analisar(historico)

        if entrada:
            entrada_ativa = entrada
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
