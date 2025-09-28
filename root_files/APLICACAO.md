
### **SISTEMA.md**

# **Documentação do Projeto SGHSS**

## 1\. Sobre o Docker

### **1.1. Abstração e Containers**

O Docker não cria máquinas virtuais, mas sim **containers**, que são ambientes isolados e leves. Eles compartilham o sistema operacional do host, o que os torna mais rápidos e eficientes do que VMs. Um container é uma abstração da **aplicação**, garantindo que ela funcione da mesma forma em qualquer ambiente.

### **1.2. Principais Comandos em Docker**

  * `docker compose up`: Inicia todos os serviços no `docker-compose.yml`.
  * `docker compose up --build`: Inicia os serviços e reconstrói as imagens antes.
  * `docker compose down`: Para e remove os contêineres, mas mantém os volumes.
  * `docker compose down --volumes`: Para e remove os contêineres e os volumes, limpando completamente o ambiente.
  * `docker compose ps`: Lista os contêineres em execução.
  * `docker compose logs [serviço]`: Exibe os logs de um serviço específico.
  * `docker compose run --rm [serviço] [comando]`: Executa um comando em um contêiner temporário, ideal para tarefas administrativas (como migrações).
  * `docker compose exec -it [serviço] [comando]`: Executa um comando em um contêiner em execução, permitindo acessar o shell (`bash`).
  * `docker network ls`: Permite virificar as redes criadas pelo Docker. rm -nome_da_rede- para remover.


### **1.3. Configurando Dockerfile**

O `Dockerfile` é a receita para construir a imagem de um container.

  * `FROM python:3.9-slim`: Define a imagem base.
  * `WORKDIR /app`: Define o diretório de trabalho.
  * `COPY requirements.txt .`: Copia as dependências para o cache do Docker.
  * `RUN pip install ...`: Instala as dependências.
  * `COPY . .`: Copia o código-fonte para a imagem.
  * `EXPOSE [porta]`: Documenta a porta que o container usa internamente.
  * `CMD ["comando"]`: Define o comando que será executado quando o container iniciar.

### **1.4. Configurando Docker Compose**

O `docker-compose.yml` orquestra múltiplos contêineres em uma única rede.

  * **`services`**: Lista os contêineres da aplicação.
  * **`build: ./serviço`**: Indica onde o Docker deve procurar o `Dockerfile`.
  * **`ports: "host:container"`**: Mapeia a porta do host para a porta interna do container.
  * **`depends_on`**: Garante que as dependências sejam iniciadas na ordem correta.
  * **`volumes`**: Persiste os dados dos bancos de dados e sincroniza o código local com o container.

### **1.5. Portas e Leitura do Docker**

  * A porta **interna** é definida no **`Dockerfile` (`EXPOSE`)** e na segunda parte do `ports` no `docker-compose.yml` (`:8001`).
  * A porta **externa** é definida na primeira parte do `ports` (`8002:`). Essa é a porta que você acessa via `localhost`.
  * Existe diferença em EXPOSE e --publish | EXPOSE porta, por onde o docker vai comunicar; --publish portaExt, por onde vai acessar no localhost:portaExt, como a imagem tem o EXPOSE ao acessar a docker o tratamento interno não importa.
  * porta_local:porta_container
  * Comando para rodar Docker em porta específica:
    * docker run -d -p portaLocalHost:portaInterna sua_imagem_app
    * docker run -P <imagem_docker> -> esse comando usa a porta interna do EXPOSE,  e escolhe uma aleatória para o Localhost. Para usar o conteiner é preciso rodar `docker ps` para descobrir qual foi a porta usada, só depois `localhost:<portausada>`

#### **1.5.1. Conflito de portas internas**
  * Contêineres são Isolados, mas os Recursos Internos Têm Limites quando usar um **Namespace** com Docker Compose.
  * o Docker isola (recursos de sistema) e o que ele compartilha (o kernel e as regras de rede).

  1. **Namespaces no Docker Compose e Projetos Separados**
  * Isolamento de Namespace de Rede: O Docker Compose é o orquestrador que garante o isolamento.

  * Um único arquivo docker-compose.yml cria um único namespace de rede (uma rede virtual privada) para todos os seus serviços, onde o conflito de portas internas é possível.

  * **Dois projetos diferentes** (rodando em pastas separadas, com seus próprios docker-compose.yml) iniciam em Namespaces de Rede separados e, portanto, **não há conflito de portas internas**.

  * Contêineres são unidades isoladas, cada um com seu próprio sistema de arquivos, processos e interfaces de rede. No entanto, o Docker (e o Kubernetes) usa um modelo chamado contenção de recursos ou namespace, não uma máquina virtual completa.
  
  2. **O Ponto de Conflito: A Porta TCP/IP**
  * Se dois serviços (contêineres) estão na mesma rede (padrão no Docker Compose), eles não podem rodar aplicativos que tentam escutar na mesma porta TCP/IP interna (ex: dois apps tentando usar a porta 8000). Isso gera um erro, pois o kernel do sistema operacional só permite que um único processo aloque aquele recurso lógico.
  * Conflito: Se o Serviço 1 tenta iniciar um servidor que escuta na **porta 8000** e o Serviço 2 tenta iniciar outro servidor que também escuta na **porta 8000**, o kernel do sistema operacional dirá: **"A porta 8000 já está em uso por outro processo"**.

  3. **Dois projetos, cada um com seu próprio docker-compose.yml**

  * Cria uma Rede Exclusiva: Para o Projeto A, ele cria uma rede interna (ex: projeto_a_default).

  * Cria Outra Rede Exclusiva: Para o Projeto B, ele cria outra rede interna (ex: projeto_b_default).
  * é possiǘel dois conteiner usar a mesma porta **se estão em docker-compose diiferente.**
  

### **1.6. Comandos Internos do Docker**

  * **`volumes`**: Cria volumes nomeados para persistir dados fora do ciclo de vida dos containers, evitando perda de dados.
  * **`depends_on`**: Garante a ordem de inicialização dos serviços.
  * **`environment`**: Define variáveis de ambiente para os containers, como credenciais de banco de dados.

### **1.7. Construção com Compose e Manutenção**

  * **Desenvolvimento**: Use `docker compose up` com **`volumes`** para sincronizar código em tempo real, sem reconstruir a imagem a cada alteração.
  * **Produção**: Use `docker compose up` sem `volumes` e com o comando **`COPY`** no Dockerfile para criar uma imagem autocontida e portátil.
  * **Rebuildar Após Alteração**: Use `docker compose up -d --no-deps --build authentication-service` ou `docker compose up --build -d --no-deps sghss-monolith` para recriar a imagem de uma docker específica, nesse caso monolith. Use `-d` para manter o serviço em backstage. Use **--no-deps** para não recriar as dependências.
  * **Desfazer as Dockers que estão rodando**: Usar `docker compose down --volumes` para e remove os contêineres.
  * **LIMPEZA DE IMAGENS E ARQUIVOS**: Para retirar todo caches e garantir que o ambiente comece novamente, USE: `docker compose down --volumes --rmi all`; ele remove as imagens padrão, remove as versões internas do compose latest etc...
  * **LIMPEZA TOTAL**
  * `docker system prune -a --force` Force uma limpeza de sistema mais profunda, que remove redes, caches e imagens não utilizados. (Use com cautela, pois isso limpará tudo que não estiver em uso, incluindo outras imagens e caches **não relacionados ao seu projeto.**)
  

### **1.8. Solicitação de Serviços**

  * **`curl`**: Comando de terminal para testar APIs.
  * **`docker compose run`**: Para tarefas administrativas.
  * **`docker compose exec`**: Para executar comandos em containers já em execução.

### **1.9. Acompanhamento por Log**

Logs do Docker (`docker compose logs [serviço]`) são a única forma de depurar erros em ambientes de containers. Telas "travadas" geralmente indicam que o container está ocioso, aguardando conexões.

### **1.10. MIGRAÇÕES**

Garanta que o ambiente está rodando:
Bash

`docker compose up -d`

#### **1.10.1. MIGRAÇÃO AUTOMÁTICA**

Ver arquivo root_files/APLICACAO/0002_alter_user_options_alter_user_managers_and_more.py

Crie e aplique as migração específica de patients:
Bash

`docker compose run --rm sghss-monolith python manage.py makemigrations patients`

Isso irá gerar os arquivos de migração.
Bash

`docker compose run --rm sghss-monolith python manage.py migrate`

Isso irá aplicar as migrações no banco de dados.

Certifique-se de que os contêineres *específico* do banco de dados estejam em execução:
Bash

`docker compose up -d db-postgres`

#### **1.10.2. MIGRAÇÃO MANUAL**

Ver arquivo root_files/APLICACAO/0003_auto_20250925_1246.py

Neste caso, não podemos contar com o Django para fazer a migração automática. Precisamos criar uma migração manual que converta os tipos de forma explícita. O processo será dividido em duas etapas:

    Converter a coluna id para um formato que possa ser convertido.

    Preencher a coluna com os UUIDs.

Vamos criar um novo arquivo de migração vazio para o seu app accounts.

Passo 1: Criar um Arquivo de Migração Vazio

No seu terminal, execute o seguinte comando para criar um arquivo de migração vazio no app accounts:
Bash

docker compose run --rm sghss-monolith python manage.py makemigrations accounts --empty

Isso criará um arquivo vazio em sghss-monolith/accounts/migrations/. O nome do arquivo será algo como 0002_auto_....py.

Passo 2: Adicionar a Lógica da Migração

Agora, edite o novo arquivo de migração que você acabou de criar. Adicione o seguinte código dentro da lista operations:

Dentro da IDE que está utilizando, procurar o arquivo de migração, nesse caso usamosa pasta accounts"->"migrations".

Alterar esse arquivo com o código que temos interesse em usar.
Após essa alteração, você precisa rodar a migração novamente.
Bash

`docker compose run --rm sghss-monolith python manage.py migrate`

O Django agora executará essa migração manual. Depois de concluída, a sua tabela de users terá o tipo de dados uuid na coluna id, resolvendo o problema de uma vez por todas.

#### **1.10.3. MIGRAÇÃO MANUAL BRUTA - NO SQL**

Ver arquivo sghss-monolith/accounts/migrations/0002_auto_20250925_1751.py

solução anterior, migração manual, que usava o AlterField, não funcionou como esperado porque o PostgreSQL ainda tentou fazer uma conversão direta, o que ele não consegue.

Para resolver este problema de uma vez por todas, precisamos adotar uma abordagem mais avançada: criar uma migração manual com SQL bruto.

Migração com SQL Explícito

Vamos criar um novo arquivo de migração vazio e usar a operação RunSQL do Django para executar os comandos SQL necessários.

Primeiro, garanta que seu ambiente Docker esteja rodando com docker compose up -d.

    Crie um novo arquivo de migração vazio:
    Bash

`docker compose run --rm sghss-monolith python manage.py makemigrations accounts --empty`

Edite o novo arquivo de migração:

Abra o novo arquivo de migração que foi criado (ele terá um nome como 0004_...py) e substitua todo o conteúdo dentro da lista operations pelo seguinte código:

! accounts/migrations/0004_....py

Execute a migração:
Bash

`docker compose run --rm sghss-monolith python manage.py migrate`

Essa abordagem é mais complexa, mas garante que a conversão do tipo de dado seja feita de forma explícita, evitando o erro do PostgreSQL. É uma técnica avançada, e o fato de você estar enfrentando e resolvendo isso é uma prova de que seu aprendizado está em um nível profissional.

#### **1.10.4. DESFAZER MIGRAÇÃO - COM ERRO
Apagar o Arquivo de Migração com Erro

O registro de migrações do Django está no seu banco de dados. Para consertar, precisamos:

  1. Dizer ao Django para "reverter" a migração 0003.py (mesmo que ela tenha falhado).

  2. Apagar o arquivo 0003.py do seu sistema de arquivos.

  3. Executar a migração 0004.py que contém a correção.

No seu terminal, navegue até o diretório do seu projeto monolito e execute o seguinte comando:
Bash
`docker compose run --rm sghss-monolith python manage.py migrate accounts 0002_...`


Substitua 0002_... pelo nome da sua migração imediatamente anterior à 0003.py. Isso irá dizer ao Django para reverter a migração falha.

Em seguida, apague o arquivo sghss-monolith/accounts/migrations/0003_...py do seu sistema de arquivos.

Agora, o seu manage.py migrate tentará aplicar a sua migração 0004_...py que contém a lógica de correção. Isso deve resolver o problema e finalmente migrar o tipo de dado uuid para o seu banco de dados.

Siga estes passos na ordem para consertar as migrações:

**Passo 1: Reverter para a Migração Anterior**

    Este comando reverterá o estado do seu banco de dados para a migração anterior à 0003, desfazendo qualquer alteração que ela possa ter feito.

Bash
`docker compose run --rm sghss-monolith python manage.py migrate accounts 0002_...`

**Passo 2: Apagar o Arquivo Com Erro**

    Remova o arquivo 0003_...py da sua pasta sghss-monolith/accounts/migrations/.

**Passo 3: Criar a Nova Migração Vazia**

    Este comando criará o arquivo 0004_...py.
Bash
`docker compose run --rm sghss-monolith python manage.py makemigrations accounts --empty`

**Passo 4: Inserir a Lógica Corrigida**

    Edite o novo arquivo 0004_...py e adicione a lógica de migração com RunSQL que definimos anteriormente.

**Passo 5: Aplicar a Nova Migração**

    Este comando irá aplicar a migração corrigida no seu banco de dados.

Bash
`docker compose run --rm sghss-monolith python manage.py migrate`
-----

## 2\. Serviço de API

### **2.1. Como a API Funciona**

A API (Application Programming Interface) é um conjunto de regras que permite que diferentes serviços se comuniquem. As APIs REST usam os verbos HTTP (GET, POST, PUT, DELETE) para realizar operações de CRUD (Criar, Ler, Atualizar, Deletar).

### **2.2. Como Configurar a Rota da API**

A configuração da rota é o ato de mapear um URL a uma função no seu código que irá processar a requisição.

**Exemplo (Django):**

```python
# urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('api/patients/register/', views.register_patient_view, name='register-patient'),
]
```

### **2.3. Serviço de IA**

  * **Comunicação:** O serviço de IA atua como um microsserviço, expondo uma API para o monolito.
  * **Solicitação:** A requisição para a API de IA é feita via HTTP.

**Exemplo com CURL:**

```bash
curl -X POST http://localhost:8003/api/ai/chat -d '{"prompt": "O que é um prontuário médico?"}'
```

### **2.4. Django**

  * **Configuração:** O Django exige que você configure o `settings.py` com `SECRET_KEY`, `ALLOWED_HOSTS` e `ROOT_URLCONF` para funcionar corretamente.
  * **Comunicação com o BD:** A comunicação é feita via ORM, que traduz o código Python em consultas SQL.
  * **Solicitação:** Para acessar a API do Django no Docker, use `curl` na porta do host mapeada no `docker-compose.yml`.

-----

## 3\. Problemas que foram encontrados e resolvidos

  * **`Unresolved reference`**: Resolvido ativando o ambiente virtual corretamente e configurando o interpretador no PyCharm.
  * **`Command not found`**: Resolvido com o uso do `docker compose` (sem hífen).
  * **`Authentication failed`**: Resolvido corrigindo as credenciais no código e no `docker-compose.yml` e especificando o `authenticationDatabase`.
  * **`No such file or directory`**: Resolvido criando os arquivos `manage.py` e corrigindo o caminho no `Dockerfile`.
  * **Erros de Configuração do Django**: Resolvidos com a configuração de `ALLOWED_HOSTS`, `SECRET_KEY` e `ROOT_URLCONF`.
  * **`DoesNotExist`**: Resolvido com a migração correta dos modelos de dados.
  * **`relation "..." does not exist`**: Resolvido com a aplicação das migrações do Django.

## 4\. Comandos para Solicitar Serviços do Docker

  * **Para API de Autenticação:**
    `curl -X POST http://localhost:8060/api/auth/login`
  * **Para API de IA:**
    `curl -X POST http://localhost:8070/api/ai/chat`
  * **Para API de Cadastro de Paciente:**
    `curl -X POST http://localhost:8050/api/patients/register/`

-----

Este documento resume todo o conhecimento que você adquiriu, do setup à depuração, e servirá como um guia completo para o seu projeto.