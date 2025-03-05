# Importações
import requests

# Variáveis
url = "http://localhost"
webhook = "UrlDoSeuWebhook"
log_file = "/var/log/monitoramento.log"

# Função de registrar o log no arquivo monitoramento.log 
def log(mensagem):
    # Abre o arquivo de log no modo "a" (append), o que garante que as novas mensagens sejam adicionadas ao final do arquivo, sem sobrescrever os logs anteriores
    with open(log_file, "a") as log:
        log.write(mensagem + "\n")  # Escreve a mensagem no arquivo 

# Função para verificar se o site esta disponível 
def monitoramento():
    try:
        # Faz uma requisição GET para a URL definida com um timeout de 10 segundos
        res = requests.get(url, timeout=10)
        status_code = res.status_code # Obtém o código de status da resposta
        
        # Se o código do site for 200, ele está disponível
        if status_code == 200:
            mensagem = "✅ Site OK - Código de Status: {status_code}"
            discord_notificacao(mensagem)
        else:
            # Se o código for diferente de 200, ele está indisponível
            mensagem = f"⚠️ Site retornou um status inesperado: {res.status_code}"
            discord_notificacao(mensagem) # Envia uma notificação para o Discord
        log(mensagem) # Registra a mensagem no log
        
    # Caso ocorra um erro de conexão, trata a exceção e registra a falha
    except requests.RequestException as e:
        mensagem = f"❌ Erro ao acessar o site: {e}"
        discord_notificacao(mensagem)  # Envia uma notificação para o Discord
        log(mensagem) # Registra a mensagem no log
        
# Função para enviar uma notificação ao Discord em caso de erro 
def discord_notificacao(mensagem):
    # Monta o payload com a mensagem de erro, pois o webhook do Discord espera um objeto JSON
    data = {"content": mensagem}
    requests.post(webhook, json=data) # Envia a mensagem para o webhook do Discord
    
# Chamada da função principal
if __name__ == "__main__":
    monitoramento()