
# ** Como acessar o arquivo do Banco de Dados

Você não consegue ver os arquivos do banco de dados na sua máquina porque o Docker os armazena em um local especial, fora do sistema de arquivos do seu projeto. Isso acontece por causa dos volumes nomeados.

Como os Dados são Armazenados

A linha volumes: no seu docker-compose.yml é a chave.

    postgres_data:/var/lib/postgresql/data

    mongodb_data:/data/db

Essa sintaxe diz ao Docker para criar um volume gerenciado chamado postgres_data e outro chamado mongodb_data. O Docker armazena os dados do banco de dados nesses volumes, que ficam em um local do sistema de arquivos que é gerenciado pelo próprio Docker. Isso garante que os dados persistam mesmo que você remova os contêineres.

# ** Como fazer Bakcup do Banco de Dados

A forma correta de fazer backup não é copiando arquivos, mas usando os utilitários de backup que vêm com os próprios bancos de dados, diretamente do contêiner.

## Para PostgreSQL (usando pg_dump)

Este comando cria um backup do banco de dados sghss_db e salva em um arquivo local na sua máquina.
Bash

``` docker exec db-postgres pg_dump -U user sghss_db > sghss_db_backup.sql ```

## Para MongoDB (usando mongodump)

Este comando cria um backup do banco de dados auth_db e o salva em uma pasta local.
Bash

```docker exec db-mongodb mongodump --db auth_db --out /backup --username user --password password```

Você pode, então, copiar a pasta /backup do contêiner para a sua máquina.

Essa abordagem garante que você esteja fazendo um backup consistente e válido, usando as ferramentas certas para cada banco de dados.