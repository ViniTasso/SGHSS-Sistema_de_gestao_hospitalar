
# Módulo principal do Projeto

Neste módulo está centralizado todas as operações e requisições com DJANGO!

## O QUE É O DJANGO?
O Django é um framework web de alto nível e de código aberto para Python. Ele foi criado para simplificar o desenvolvimento de sites complexos e dinâmicos, seguindo a filosofia de "baterias incluídas" (batteries included), ou seja, ele já vem com a maioria das ferramentas que você precisa para criar uma aplicação web, como um sistema de ORM (Mapeamento Objeto-Relacional), um template engine, e um painel de administração automático.

## MVT (Model-View-Template)
O Django segue um padrão de arquitetura conhecido como MVT (Model-View-Template), que é uma variação do famoso padrão MVC (Model-View-Controller). A ideia é separar as responsabilidades do seu código para que cada parte se encarregue de uma tarefa específica.

### Model: 
É a camada de dados. O Model define a estrutura do seu banco de dados, ou seja, como os dados são armazenados. Em vez de escrever código SQL, você cria classes Python que representam as tabelas do seu banco de dados. Por exemplo, você pode ter uma classe Produto com atributos como nome, preço e descrição. O Django ORM (Object-Relational Mapper) cuida de traduzir essas classes para o código SQL necessário para criar, ler, atualizar e excluir dados no banco.

### View: 
É a camada de lógica. A View recebe as requisições HTTP e processa a lógica de negócio da sua aplicação. É aqui que você define o que acontece quando um usuário acessa uma URL. Por exemplo, uma View pode buscar dados no Model, processá-los e passá-los para o Template. Em essência, a View é a "ponte" entre o Model e o Template.

### Template: 
É a camada de apresentação. O Template define a interface de usuário (UI) da sua aplicação, que é o que o usuário vê no navegador. Ele é um arquivo HTML que pode incluir placeholders e lógica simples para exibir dados dinâmicos vindos da View. O Django tem seu próprio template engine que facilita a criação de páginas web com conteúdo dinâmico.

## Como uma requisição web é processada no Django?
Para entender o fluxo completo, imagine que um usuário acessa a URL de uma página de produtos do seu site:

### URL Dispatcher (urls.py): 
O Django recebe a requisição e o primeiro ponto de contato é o arquivo urls.py. Ele mapeia a URL acessada pelo usuário para a View correta que irá processar essa requisição.

### View (views.py): 
A View associada à URL é executada. Ela contém a lógica para lidar com a requisição. A View interage com o Model para buscar, filtrar ou salvar dados no banco de dados.

### Model (models.py): 
O Model é usado para interagir com o banco de dados. O ORM do Django converte o código Python da View em instruções SQL. Por exemplo, se a View pedir para buscar todos os produtos, o Model faz essa busca no banco de dados.

### Template (templates/*.html): 
Depois que a View obtém os dados do Model, ela os envia para o Template apropriado. O template engine do Django preenche os espaços reservados no arquivo HTML com os dados dinâmicos.

### Resposta HTTP: 
Finalmente, o Django retorna a página HTML processada para o navegador do usuário, que a exibe na tela.

## Por que DJANGO? Qual vantagem?
Painel de administração (Admin Site): O Django gera automaticamente um painel de administração robusto, que permite a você gerenciar os dados dos seus Models de forma fácil, sem precisar escrever quase nenhuma linha de código.

ORM: O Mapeador Objeto-Relacional do Django simplifica a interação com o banco de dados, permitindo que você use classes e objetos Python em vez de SQL.

URL Dispatcher: É um sistema poderoso para mapear URLs para suas Views, o que torna as URLs mais limpas e legíveis.

Segurança: O Django já vem com recursos de segurança integrados para proteger contra ameaças comuns, como injeção de SQL, Cross-Site Scripting (XSS) e Cross-Site Request Forgery (CSRF).

Sistema de autenticação: Um sistema completo de autenticação e permissões de usuário já está pronto para ser usado.