from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN", "")
ID_NUMERO = os.environ.get("ID_NUMERO", "")
LINK_COMUNIDADE = "https://chat.whatsapp.com/JPvLwPHZcc42v8JDdHgqAe"

def enviar_msg(para, texto):
    if not TOKEN or not ID_NUMERO:
        return
    url = f"https://graph.facebook.com/v20.0/{ID_NUMERO}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": para, "text": {"body": texto}}
    requests.post(url, headers=headers, json=data)

@app.route("/", methods=["GET"])
def home():
    return "Bot do Vitor online! ✅"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == "vitor123":
            return request.args.get("hub.challenge")
        return "Erro", 403
    try:
        entry = request.json['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            de = msg['from']
            texto = msg.get('text', {}).get('body', '').lower()
            if texto in ["oi", "olá", "ola", "menu", "inicio", "início"]:
                resposta = f"Olá! 👋 Aqui é do Vitor!\n\nTenho uma Comunidade exclusiva com ofertas e avisos em primeira mão.\n\n👉 Digite:\n1️⃣ - Quero entrar na Comunidade\n2️⃣ - Falar com o Vitor"
            elif texto == "1":
                resposta = f"Boa! Entra aqui: 👇\n{LINK_COMUNIDADE}"
            elif texto == "2":
                resposta = "Perfeito, me diz o que precisa? 😊"
            else:
                resposta = f"Digite *oi* para ver o menu ou entre direto: {LINK_COMUNIDADE}"
            enviar_msg(de, resposta)
    except:
        pass
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
