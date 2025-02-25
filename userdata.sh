#!/bin/bash
# Atualiza o sistema e instala o nginx
sudo yum update -y && sudo yum install nginx -y

# Instala o cron e ativa o serviço
sudo yum install cronie -y
sudo systemctl enable crond --now

# Cria a página HTML de exemplo
sudo cat << 'EOF' > /usr/share/nginx/html/index.html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto do Estágio - Giovana</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            width: 80%;
            margin: auto;
            text-align: justify;
        }
        h1 {
            color: #4CAF50;
        }
        .content {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .footer {
            margin-top: 30px;
            font-size: 0.8em;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Projeto: Configuração de Servidor Web com Monitoramento</h1>
        <div class="content">
            <h2>Objetivo do Projeto</h2>
            <p>Desenvolver e testar habilidades em Linux, AWS e automação de processos através da configuração de um ambiente de servidor web monitorado.</p>

            <h3>Tecnologias Utilizadas</h3>
            <ul>
                <li>AWS EC2</li>
                <li>Linux</li>
                <li>Nginx</li>
            </ul>
        </div>
        <div class="footer">
            <p>Desenvolvido por Giovana da Silva Albanês Santos</p>
        </div>
    </div>
</body>
</html>
EOF

# Habilita e inicia o serviço Nginx
sudo systemctl enable nginx --now

# Cria o script de monitoramento em /opt/monitoramento.py
sudo cat << 'EOF' > /opt/monitoramento.py
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
EOF

# Dá permissão de execução para o script
sudo chmod +x /opt/monitoramento.py

# Garante que o arquivo de log existe e dá permissão para o ec2-user
sudo touch /var/log/monitoramento.log
sudo chown ec2-user:ec2-user /var/log/monitoramento.log

# Adiciona o cron job para rodar o script a cada 1 minuto
(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/python3 /opt/monitoramento.py >> /var/log/monitoramento.log 2>&1") | crontab -
