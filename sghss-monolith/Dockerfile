# Usa uma imagem Python leve como base para o container.
# O "slim" garante que a imagem seja menor, ideal para produção.
FROM python:3.11-slim

# Define o autor/mantenedor
LABEL maintainer="Vinícius Tasso RU4632546"
LABEL description="SGHSS - Django Monolith Backend"

# Define variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Define o diretório de trabalho dentro do container.
# É aqui que o nosso código será copiado.
WORKDIR /app

# Instala dependências do sistema necessárias
# - build-essential: para compilar algumas bibliotecas Python
# - libpq-dev: necessário para psycopg2 (PostgreSQL)
# - gettext: para internacionalização do Django
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos primeiro.
# Isso aproveita o cache do Docker. Se os requisitos não mudarem,
# esta etapa não será executada novamente.
COPY requirements.txt .

# Instala as dependências Python. O comando "--no-cache-dir"
# ajuda a manter o tamanho final da imagem pequeno.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container.
COPY . .

# Cria os diretórios necessários
# Cria diretórios para arquivos estáticos, mídia e LOGS
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chmod 755 /app/logs

# Expõe a porta que o servidor de desenvolvimento do Django irá usar.
EXPOSE 8000

# Define o comando para iniciar a aplicação quando o container for iniciado.
# Para desenvolvimento, usamos o servidor embutido do Django. python manage.py runserver
# Em produção, usaríamos `gunicorn sghss_core.wsgi:application`
# O "0.0.0.0" garante que o servidor seja acessível de fora do container.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
