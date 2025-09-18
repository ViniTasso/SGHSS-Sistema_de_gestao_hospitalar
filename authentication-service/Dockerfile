# 1. Usa uma imagem oficial do Python como base.
# A versão 3.9-slim é leve e contém apenas o necessário.
FROM python:3.9-slim

# 2. Define o diretório de trabalho dentro do contêiner.
# É o local onde o nosso código será copiado e executado.
WORKDIR /app

# 3. Copia o arquivo de dependências para o contêiner.
# Copiar o requirements.txt primeiro otimiza o cache do Docker.
# Se as dependências não mudarem, este passo não será re-executado em builds futuras.
COPY requirements.txt .

# 4. Instala as dependências listadas no requirements.txt.
# O argumento '--no-cache-dir' ajuda a reduzir o tamanho da imagem final.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o restante do código da aplicação para o diretório de trabalho.
# O ponto '.' se refere ao diretório atual no host (authentication-service).
COPY . .

# 6. Expõe a porta que a aplicação Flask irá usar.
# A porta 8001 foi definida no nosso docker-compose.yml para este serviço.
EXPOSE 8001

# 7. Define o comando para iniciar a aplicação.
# O "flask run" é o comando padrão para o servidor de desenvolvimento do Flask.
# O "--host 0.0.0.0" permite que o servidor seja acessível de fora do contêiner.
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8001"]