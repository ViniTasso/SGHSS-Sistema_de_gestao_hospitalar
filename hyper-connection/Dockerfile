# --------------------------------------------------------------------------------
# FASE 1: BUILD (Compilação do Código Java)
# O objetivo é transformar o código-fonte em um arquivo JAR executável.
# --------------------------------------------------------------------------------
# O AS builder dá um nome a essa fase.
# Permite a técnica de Multi-Stage Build, mantendo a imagem final pequena.
# A imagem base. Tem o JDK (Java Development Kit) e o Maven instalado.
FROM maven:3.9-eclipse-temurin-21 AS builder
MAINTAINER Vinicius Tasso
# Define o diretório de trabalho dentro do container
WORKDIR /app

# 1. Copia o arquivo de configuração do Maven primeiro.
# Isso permite ao Docker Cache as dependências se o pom.xml não mudar, acelerando o build.
COPY pom.xml .

# 2. Copia a estrutura de pastas do código-fonte (src)
COPY src src

# 3. Executa a compilação e empacotamento.
#Cria um volume de cache para o Maven.
# O -DskipTests garante que ele não rode os testes, economizando tempo na build.

RUN --mount=type=cache,target=/root/.m2 mvn clean package -DskipTests -X
# o código abaixo Causa a corrupção do JAR
#RUN mkdir -p build/dependency && (cd build/dependency; jar -xf ../../target/*.jar)

# O cache do mount ajuda a reusar dependências, tornando builds repetidas mais rápidas.

#Teste da compilação
#RUN ["ls", "-l", "target/"]
# --------------------------------------------------------------------------------
# FASE 2: RUNTIME (Execução da Aplicação)
# O objetivo é usar uma imagem mais leve, que só tem o Java Runtime (JRE).
# --------------------------------------------------------------------------------
# Usamos a imagem JRE (Java Runtime Environment) que é muito menor que o JDK (Developer Kit)
# LINHAS DE DIAGNÓSTICO AVANÇADO (Após a compilação):
# # 1. Mostra onde estamos (deve ser /app)
# RUN pwd
# # 2. Mostra o conteúdo da pasta de trabalho (deve mostrar 'target/')
# RUN ls -l
# # 3. Lista o conteúdo da pasta 'target' (onde o JAR deve estar)
# RUN ls -l target/
# RUN ls -laR / > /tmp/build_log.txt 2>&1
# --------------------------------------------------------------------------------


FROM eclipse-temurin:21-jre-alpine

# Define o volume de trabalho
# WORKDIR /app
# RUN ["echo", "/tmp/build_log.txt"]

# # NOVO: BOA PRÁTICA DE SEGURANÇA E CORREÇÃO DE PERMISSÃO
# # Cria um grupo e um usuário 'spring' com baixo privilégio
# RUN addgroup --gid 1000 spring && adduser -u 1000 -G spring -s /bin/sh -D spring
# #
# ## Garante que o usuário 'spring' possa ler/escrever no diretório
# RUN chown -R spring:spring /app
# #
# ## Troca o usuário que irá executar o ENTRYPOINT para 'spring'
# USER spring



# 1. Copia o arquivo JAR compilado da 'builder' stage
# O nome do JAR será 'ai-proxy-0.0.1-SNAPSHOT.jar' se você não mudou o nome no pom.xml
# Usamos um wildcard (*) para pegar qualquer JAR gerado.
#Quando você não usa o parâmetro --from, o Docker assume que o caminho de origem (/app/build/dependency/) é um local no seu disco rígido, dentro da pasta onde você executa o docker compose up.
#COPY --from=builder /app/target/ai-proxy-1.0-SNAPSHOT.jar app.jar
#COPY --from=builder /app/app.jar app.jar

RUN ["ls", "-a"]
#COPY /app/target/*.jar app.jar
#COPY /app/build/dependency/*.jar app.jar
#COPY --from=builder /app/build/dependency/ app.jar

# ----------------------------------------------------------------------
# 2. CORREÇÃO DE PERMISSÃO: Adicione a correção de permissão.
# Esta linha evita o problema de 'access denied' em imagens Alpine.


# 3. Usuário de Baixo Privilégio (Melhor Prática)
#RUN addgroup -S spring && adduser -S spring -G spring
#RUN chown -R spring:spring /app
#RUN chmod 755 app.jar
#USER spring
# RUN addgroup -S spring && adduser -S spring -G spring

# 2. PERMISSÃO E DONO: MUDANÇA DE DONO E CHMOD EM UM PASSO SÓ
# O `app.jar` agora está acessível. O `&&` garante que se um falhar, todos falham.
#RUN chown -R spring:spring /app && chmod 755 /app/target/app.jar
COPY --from=builder /app/target/app.jar app.jar
# ----------------------------------------------------------------------
# O RESTO DO SEU DOCKERFILE
# ----------------------------------------------------------------------

# USER spring # O usuário que rodará a aplicação
# 2. Expõe a porta que o Spring Boot usa (definida em application.properties)
EXPOSE 8003

# 3. Comando que inicia a aplicação.
# O Java executa o JAR.
#RUN ls -l @echo

ENTRYPOINT ["java", "-jar", "app.jar"]
#RUN chmod -R 755 /app.jar