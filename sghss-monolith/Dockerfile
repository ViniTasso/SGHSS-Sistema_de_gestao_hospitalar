# Usa uma imagem Python leve como base para o container.
# O "slim" garante que a imagem seja menor, ideal para produção.
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container.
# É aqui que o nosso código será copiado.
WORKDIR /app

# Copia o arquivo de requisitos primeiro.
# Isso aproveita o cache do Docker. Se os requisitos não mudarem,
# esta etapa não será executada novamente.
COPY requirements.txt .

# Instala as dependências Python. O comando "--no-cache-dir"
# ajuda a manter o tamanho final da imagem pequeno.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container.
COPY . .

# Expõe a porta que o servidor de desenvolvimento do Django irá usar.
EXPOSE 8000

# Define o comando para iniciar a aplicação quando o container for iniciado.
# Para desenvolvimento, usamos o servidor embutido do Django.
# O "0.0.0.0" garante que o servidor seja acessível de fora do container.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]