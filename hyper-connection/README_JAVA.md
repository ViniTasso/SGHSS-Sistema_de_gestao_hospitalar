
Esse módulo servira apenas para estudo.
Será recebido uma requisição POST do monolith, e solicitado ao ai-service.
Fazendo apenas a conexão entre essas duas ferramentas, request to request.

Campo	   Valor Sugerido	Explicação
Name	   hospital-ai-proxy	Nome do projeto (pasta).
Type	Maven - Para Gerenciador de dependências.
Group	com.hospital	Geralmente um domínio reverso (ex: com.suaempresa)
Artifact	ai-proxy	Nome do módulo (é a base do pacote raiz).
Package name	com.hospital.aiproxy	A base para todos os arquivos Java.

No Intellij IDEA Ultimate 
    Procurar por Spring Web 
    Facilita criar API e, inclui o Jackson (para JSON) e o Tomcat (servidor embutido).

AiProxyApplication.java é a classe principal do aplicativo Spring Boot
Geralmente criada automaticamente quando configura o Spring Initializr

# Alterações no pom.xml - MAVEN
**Reimport All Maven Projects**
O pom.xml mostra todas dependencias do projeto.
Após alterar o pom.xml, ir até o lado direito, e sincronizar pelo controle do Maven. 

# Requisição 
curl -X POST http://localhost:8081/api/v1/ai-proxy/chat -H "Content-Type: application/json" -d '{"prompt": "Quais são as regras de privacidade de dados em hospitais?"}'

## Spring Boot e Jackson
Quem vai tratar os dados que vão ser usados é essas duas bibliotecas.
Toda alteração na resposta JSON implica também na alteração do models e no AiProxyService.
- Para cada campo novo que o JSON responde, precisa fazer get/set EM CAMELCASE, mesmo que o JSON responde snakeCase
- 