# DevSecOps - Projeto Linux 

## Documentação do primeiro projeto proposto na trilha de DevSecOps no meu programa de estágio PB - 2025 

## Objetivo 
Desenvolver e testar habilidades em Linux, AWS e automação de processos através da configuração de um ambiente de servidor web monitorado.

## Requisitos Técnicos 
- Windows 11
- Amazon Linux 2023
- Instância EC2 AWS
- Nginx

## Índice
1. [Configuração do Ambiente](#configuração-do-ambiente)
2. [Configuração do Servidor](#configuração-do-servidor)
3. [Monitoramento e Notificações](#monitoramento-e-notificações)
4. [Automação e Testes](#automação-e-testes)


## 1. Configuração do Ambiente
colocar aqui oq é uma VPC 
Primeiramente, é necessário criar uma VPC para o seu ambiente. No console da AWS pesquise pelo serviço de `VPC` e criar uma nova VPC de acordo com suas necessidades como na imagem a seguir.
![alt text](image-9.png)

Continuando na configuração da VPC, ainda precisa criar as sub-redes. No seu ambiente, navegue até a sessão de subnets e crie duas públicas e duas privadas. Uma pública e uma privada na região `us-east-1a` e as outras duas na `us-east-1b`.
![alt text](image-10.png)

Após a criação das subnets, elas irão aparecer assim na sua console.
![alt text](image-11.png)

Para contribuir para a comunicação com a internet, é necessário criar um INternet Gateway e anexá-lo à VPC. Ainda no console da AWS no serviço de VPC, navegue até `Internet Gateway` e crie de acordo com suas necessidades. 
![alt text](image-12.png)

Após a criação é necessário anexá-lo à VPC. Para isso, clique no botão de `actions` e selecione `attach to VPC`.
![alt text](image-13.png)

Para permitir que as subnets públicas se comuniquem com o ambiente externo, é necessário criar uma `Route table`. Basta ir até a sessão e criar.
![alt text](image-15.png)

Entretanto, as regras não foram definidas. Logo, selecione a `Route table` criada e edite as regras. Crie uma com destination 0.0.0.0/0 e target para o `Internet Gateway` criado anteriormente.
![alt text](image-16.png)

Ainda precisa anexar as subnets públicas à essa `Route Table`. Para isso, selecione-a e navegue até `Subnet Associations`. Por fim, edite selecionando as duas subnets públicas criadas no início.
![alt text](image-17.png)

![alt text](image-18.png)


Para dar continuidade à configuração do ambiente, chegou a hora de criar a instância EC2. Mas antes é necessário criar as regras de `Security Group`. Para configurar o tráfego da EC2, há a necessidade de criar um Security group. Agora, no console da AWS pesquise pelo serviço de `EC2` e navegue até `Security Group`. Basta criá-lo de acordo com suas necessidades. No na parte de configuração de regras de entrada, criei duas, uma permitindo o tráfego HTTP para qualquer lugar, e outra SSH para o meu IP. Assim como na imagem. As regras de saída deixar o padrão.
![alt text](image-14.png)

Agora, para criar de fato a instância EC2, no console da AWS pesquise pelo serviço de `EC2`. Navegue até a sessão de `Instâncias` e crie uma de acordo com suas necessidades. No meu caso, escolhi a AMI baseada em Amazon Linux 2023.
![alt text](AMI.png)

Durante a criação da EC2, ainda é necessário passar pelas `Configurações de Rede`. Nessa parte, as configurações devem estar assim como na imagem abaixo, na VPC criada, assim como na subnet pública, com o IP automático habilitado e no security group. Além disso, vincule uma chave SSH à ela, se voê não tiver, é só criar, pois mais tarde usaremos para conectar à EC2.
![alt text](networksettings.png)

Agora todo o seu ambiente estará configurado. Por fim, basta acessar a EC2 via SSH. Para isso, selecione a EC2 e clique em `connect` como na imagem abaixo.
![alt text](connect.png)

Após isso irá aparecer o passo a passo a ser seguido como na imagem abaixo. Você pode executá-lo no `Git Bash` ou no próprio terminal do `Visual Studio Code`. Em ambos, navegue até a paste onde você baixou a sua chave SSH e execute:
![alt text](ssh.png)

Para modificar o acesso da chave SSH.
```bash
chmod 400 "suaChave.pem"
```

Para entrar na EC2
```bash
ssh -i "suaChave.pem" ec2-user@IpPublicoDaEC2
```

Pronto, você está dentro da EC2!
![alt text](image-19.png)


## 2. Configuração do servidor 
### 2.1 Instalar o servidor Nginx na EC2
Para configurar o servidor, nessa etapa é necessário instalar o servidor web Nginx na EC2. Primeiro, abra o Visual Studio COde conectado à instância EC2. Em seguida, é necessário fazer a seguinte verificação:

Para verificar se há alguma verificação pendente, execute:
```bash
sudo dnf update -y
```

Depois, basta instalar o Nginx com o seguinte comando:  
``` bash
sudo dnf install nginx -y
```

Após a instalação ser concluída, a seguinte mensagem aparecerá:
![alt text](image.png)

Entretanto, deve-se iniciar o Nginx. Como o serviço do Nginx por padrão vem desabilitado, essa ação é necessária. Para efetuar essa ações é necessário executar os seguintes comandos:
```bash
sudo systemctl start nginx
```
```bash
sudo systemctl enable nginx
```

Depois de seguir essas etapas, verifique se o serviço do Nginx está ativo na sua EC2 com:
```bash
sudo systemctl status nginx
```

A seguinte mensagem irá aparecer se o servidor estiver funcionando:
![alt text](image-2.png)

Ao fim, para testar, basta copiar o IP público da sua instância e colar no navegador. A página que deve ser exibida é: 
![alt text](image-1.png)

### 2.2 Criar uma página HTML simples
Nessa parte, você irá editar a página HTML que está no servidor de acordo com às suas necessidades. O arquivo index.html geralmete fica em `cd /usr/share/nginx/html`. Para editar o arquivo basta executar: 
```bash
sudo nano index.html
```
Depois, basta modificar como deseja e atualizar a página do navegador que as novas informaçõe serão carregadas. De acordo com as orientações do desafio, eu preciso colocar informações sobre o projeto, logo, a minha página HTML ficou assim:

![alt text](image-3.png)

## 3. Monitoramento e notificações
### 3.1 Criar um script em Python para monitorar o site
Os requisitos do script são:
Verificar se o site responde corretamente a uma requisição HTTP.
Criar logs das verificações em /var/log/monitoramento.log.
Enviar uma notificação via Discord, Telegram ou Slack se detectar indisponibilidade.

Antes de criar o script é necessário criar um arquivo de log e um servidor no Discord, pois conforme as orientações do projeto, deve existir um log das verificações do projeto e caso haja detecção de indisponibilidade do site, uma notificação deve ser enviada ao Discord pelo webhook.

No VSCode, para criar um arquivo de log, execute
```bash
sudo touch /var/log/monitoramento.log
```

Com o Discord aberto, crie um servidor com o nome de `notificações-nginx`. Para criar um webhook, clique no ícone de engrenagem ao lado do nome do servidor, clique em integrações, navegue até webhook e crie um novo com o nome de `Notificação`. É necessário copiar a URL do webhook, pois será utilizada no script.

### 3.2 Requisitos do script em Python 
O script deve ser criado com o nome de `monitoramento.py` dentro de `cd /opt`. 

Para criar o script de monitoramento:
```bash
cd /opt
sudo nano monitoramento.py
```

Agora, basta escrever o script. Deve utilizar a biblioteca `Requests` para enviar e receber informações da internet. Para importar:

![alt text](image-4.png)

Depois, deve-se armazenar em variáveis a URL do site, a URL do webhook e o caminho do arquivo de logs. Para isso, adicione as seguintes linhas no seu script
![alt text](image-5.png)

Criar uma função para registrar os logs dentro do arquivo criado anteriormente

![alt text](image-6.png)

Criar uma função para verificar se o site responde corretamente a uma requisição HTTP. A função tenta acessar o site com o requests atráves do método get passando a URL e um tempo de 10 segundos. O código de status é armazenado em uma variável. Se o código for igual a 200, uma mensagem indicando que o site está ativo é exibida. Caso contrário, dará erro, o qual é tratado com `RequestException` exibindo a mensagem de erro. A mensagem de erro também é armazenada no arquivo de log. E também se entrar dentro desse tratamento de erro, a mensagem é enviada ao Discord com a função `enviar_notificação`, que será explicada posteriormente. 
![alt text](image-7.png)

Criar a função de enviar notificação ao Discord. Nela, um dicionário é criado com as mensagens de erro, e depois enviado ao webhook por meio do método `post`como um JSON. É importante ressaltar que o Webhook espera receber os dados como um objeto JSON.

![alt text](image-8.png)





