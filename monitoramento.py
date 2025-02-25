# Importações
import requests

# Variáveis
url = "http://localhost"
webhook = "https://discord.com/api/webhooks/1339960739191853126/lFQ5uZvEtgZjx0icODuV8nLcimEDGNy35GltUYWEUP4pv9jyH0trymxqo4GCLIy8pVPa"
log_file = "/var/log/monitoramento.log"

# Função de registrar o log no arquivo monitoramento.log 
def registrar_log(mensagem):
    # Abre o arquivo de log no modo "a" (append), o que garante que as novas mensagens sejam adicionadas ao final do arquivo, sem sobrescrever os logs anteriores
    with open(log_file, "a") as log:
        log.write(mensagem + "\n")  # Escreve a mensagem no arquivo 

# Função para verificar se o site esta disponível 
def verificar_site():
    try:
        # Faz uma requisição GET para a URL definida com um timeout de 10 segundos
        res = requests.get(url, timeout=10)
        status_code = res.status_code # Obtém o código de status da resposta
        
        # Se o código do site for 200, ele está disponível
        if status_code == 200:
            mensagem = "✅ Site OK"
        else:
            # Se o código for diferente de 200, ele está indisponível
            mensagem = f"⚠️ Site retornou um status inesperado: {res.status_code}"
            enviar_notificacao(mensagem) # Envia uma notificação para o Discord
        registrar_log(mensagem) # Registra a mensagem no log
        
    # Caso ocorra um erro de conexão, trata a exceção e registra a falha
    except requests.RequestException as e:
        mensagem = f"❌ Site INDISPONÍVEL! Erro: {e}"
        enviar_notificacao(mensagem)  # Envia uma notificação para o Discord
        registrar_log(mensagem) # Registra a mensagem no log
        
# Função para enviar uma notificação ao Discord em caso de erro 
def enviar_notificacao(mensagem):
    # Monta o payload com a mensagem de erro, pois o webhook do Discord espera um objeto JSON
    data = {"content": mensagem}
    requests.post(webhook, json=data) # Envia a mensagem para o webhook do Discord
    
# Chamada da função principal
if __name__ == "__main__":
    verificar_site()