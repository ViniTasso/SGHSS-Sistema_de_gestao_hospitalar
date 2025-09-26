
# Como utilizar SQL com DOCKER
## Passo 1: Entrar no Shell do Contêiner PostgreSQL

No seu terminal, navegue até a pasta raiz do projeto (/sghss/) e execute o seguinte comando:
Bash

docker compose exec -it db-postgres bash

Este comando abre um terminal interativo dentro do contêiner do PostgreSQL.

## Passo 2: Acessar o Banco de Dados

Dentro do shell do contêiner, use o comando psql para se conectar ao banco de dados com as credenciais que definimos.
Bash

psql -U user -d sghss_db

## Passo 3: Executar a Query SQL

Agora, você pode executar o comando SQL para encontrar o usuário que você acabou de cadastrar.
SQL

SELECT * FROM patients_patient;

O patients_patient é o nome padrão da tabela que o Django cria para a sua classe Patient.


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

# Problemas Com ROLES

## Pesquisar ROLES

Digite `SELECT * FROM roles;` após acessar o banco de dados para ver as Roles.

## Cadastrar ROLES

Para Cadastrar manualmente `INSERT INTO roles (nome) VALUES ('paciente');`

## Cadastrar no Banco pelo Shell do DJANGO

### Cadastro por Shell
digite `docker compose run --rm sghss-monolith python manage.py shell`

Dentro do Shell 
`>>> from accounts.models import Role`
`>>> Role.objects.create(nome='paciente')`
`>>> exit()`

### Busca por Sheel
from accounts.models import Role
all_roles = Role.objects.all()
for role in all_roles:
    print(f"ID: {role.id}, Name: '{role.nome}'")
exit()

# Configurações de Banco de Dados

## Como visualizar o Schema de tabela no Banco de Dado

1. Usando a Visualização information_schema.columns
Essa é a forma mais padrão e portável em SQL. A visualização information_schema.columns contém metadados sobre todas as colunas de todas as tabelas em seu banco de dados.

Para ver os detalhes de uma tabela específica, use a seguinte consulta:

SQL

SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default 
FROM 
    information_schema.columns 
WHERE 
    table_name = 'nome_da_tabela' 
    AND table_schema = 'public' -- Substitua por seu schema, se for diferente
ORDER BY 
    ordinal_position;
table_name: Substitua 'nome_da_tabela' pelo nome da sua tabela (por exemplo, 'usuarios').

table_schema: O schema padrão é 'public'. Se sua tabela estiver em outro schema, use o nome correto.

2. Usando o Comando \d no psql
Se você estiver usando o terminal psql, o cliente interativo do PostgreSQL, o comando \d é a maneira mais rápida e fácil. Ele fornece uma descrição formatada da tabela, incluindo colunas, tipos, modificadores e índices.

Para usar, simplesmente digite:

Bash

\d nome_da_tabela
Exemplo:

Bash

\d produtos
Isso retornará algo como:

                  Tabela "public.produtos"
  Coluna  |         Tipo          | Modificadores | Descrição
----------+-----------------------+---------------+-------------------------
 id       | integer               | not null      |
 nome     | character varying(50) | not null      |
 preco    | numeric(10,2)         |               |
 estoque  | integer               | default 0     |
 created_at | timestamp without time zone | default now() |
Indices:
    "produtos_pkey" PRIMARY KEY, btree (id)
    
3. Consultando a Tabela do Sistema pg_catalog.pg_attribute
Para um nível mais profundo de detalhes, você pode consultar a tabela de catálogo pg_attribute. No entanto, essa abordagem é mais complexa e menos legível do que usar information_schema.

A consulta abaixo acessa a tabela pg_class para encontrar o OID (Object Identifier) da sua tabela e depois usa o OID para buscar as colunas em pg_attribute:

SQL

SELECT 
    a.attname AS column_name,
    format_type(a.atttypid, a.atttypmod) AS data_type,
    a.attnotnull AS is_not_null
FROM 
    pg_class AS c
JOIN 
    pg_attribute AS a ON a.attrelid = c.oid
WHERE 
    c.relname = 'nome_da_tabela'
    AND a.attnum > 0 -- Evita colunas do sistema
ORDER BY 
    a.attnum;
pg_class: Tabela que armazena informações sobre tabelas, índices e views.

pg_attribute: Tabela que armazena informações sobre as colunas de tabelas.

## Como visualizar o Schema do banco de dados 

