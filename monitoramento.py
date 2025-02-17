import requests

url = "http://44.200.202.239"
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
            mensagem = "Site INDISPONÍVEL"

        registrar_log(f"{mensagem} - Código de Status: {status_code}")

    except requests.RequestException as e:
        mensagem = "Site INDISPONÍVEL"
        enviar_notificacao(mensagem)
        registrar_log(f"❌ Erro ao acessar o site: {str(e)}")

def enviar_notificacao(mensagem):
    data = {"content": mensagem}
    requests.post(webhook, json=data)

if __name__ == "__main__":
    verificar_site()