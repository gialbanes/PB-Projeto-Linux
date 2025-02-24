import requests

url = "http://localhost"
webhook = "https://discord.com/api/webhooks/1339960739191853126/lFQ5uZvEtgZjx0icODuV8nLcimEDGNy35GltUYWEUP4pv9jyH0trymxqo4GCLIy8pVPa"
log_file = "/var/log/monitoramento.log"

def registrar_log(mensagem):
    with open(log_file, "a") as log:
        log.write(mensagem + "\n")

def verificar_site():
    try:
        res = requests.get(url, timeout=10)
        status_code = res.status_code

        if status_code == 200:
            mensagem = "✅ Site OK"
        else:
            mensagem = f"⚠️ Site retornou um status inesperado: {res.status_code}"
            enviar_notificacao(mensagem)
        registrar_log(mensagem)

    except requests.RequestException as e:
        mensagem = f"❌ Site INDISPONÍVEL! Erro: {e}"
        enviar_notificacao(mensagem)
        registrar_log(mensagem)

def enviar_notificacao(mensagem):
    data = {"content": mensagem}
    requests.post(webhook, json=data)

if __name__ == "__main__":
    verificar_site()