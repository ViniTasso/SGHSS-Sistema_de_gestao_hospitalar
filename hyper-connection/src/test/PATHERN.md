A abordagem de usar forks para iniciar novos projetos a partir de um repositório modelo (ou upstream original) é muito comum.

# Entendendo o Fluxo de Trabalho com Forks e Atualizações

## Como atualizar sem perder meus arquivos
A chave para atualizar seu projeto (o fork) sem perder seus arquivos ou commits é entender como o Git lida com a fusão (merge) de histórico de diferentes ramificações ou repositórios.

O GitHub notifica você sobre as atualizações no repositório base (Projeto Base), mas a ação de puxar (trazer as mudanças) e aplicar essas atualizações no seu fork deve ser feita localmente.

Aqui está o passo a passo de como fazer isso de forma segura:

# Configurando o projeto
1. Adicionar o Repositório Base como "Upstream"
   Quando você faz o clone do seu fork pela primeira vez, o Git configura automaticamente um remoto chamado origin que aponta para o seu fork no GitHub.

Para puxar atualizações do Projeto Base original, você precisa adicioná-lo como um novo remoto. O nome padrão para o repositório original que você forkou é upstream.

No terminal, dentro do diretório do seu projeto local (Fork_1):

Bash

 **SINTAXE: git remote add <nome_do_remoto> <URL_do_repositório_original>**
git remote add upstream https://github.com/sotahtech/Projeto_Base.git
Dica: Você pode verificar se funcionou executando git remote -v. Você verá seu origin e o novo upstream.

2. Buscar e Atualizar o Repositório Local
   Depois de adicionar o upstream, você pode buscar as últimas alterações dele.

**Busca todas as branches e seus commits do repositório base (upstream)**
`git fetch upstream`
## Fusão (Merge) das Mudanças
3. Este é o passo crucial. Você irá fundir as mudanças da branch principal do Projeto Base (que geralmente é main ou master) com a sua branch local. Isso não apagará seus arquivos!

Seus commits existentes (por exemplo cod:F11, F12, F13 no seu exemplo) e os novos commits do Projeto Base (cod:P1, P2) serão combinados.

 **Garanta que você esteja na branch principal do seu fork (ex: main ou master)**
`git checkout main`

## Funde as alterações do upstream/main com a sua branch local
`git merge upstream/main`
O que Acontece com o Merge?
**Sem Conflitos:** Se as alterações no Projeto Base foram feitas em arquivos/linhas que você não modificou, o Git fará o merge automaticamente, e um novo commit de merge será criado, combinando os históricos.

**Com Conflitos:** Se as alterações no Projeto Base afetaram as mesmas linhas de código ou arquivos que você modificou, o Git interromperá o merge e informará sobre os conflitos de merge. Você terá que editar manualmente os arquivos para decidir qual versão do código manter (a sua ou a do upstream).

**Atenção:** Se houver conflitos, você precisa resolver todos eles (usando um editor de texto ou ferramenta visual), e depois fazer o commit da resolução:

Bash

### Depois de resolver os conflitos em todos os arquivos
`git add .
git commit -m "Resolvendo conflitos e atualizando com o Projeto Base"`
4. Enviar as Mudanças Atualizadas para seu Fork
   O último passo é enviar a branch local atualizada (que agora contém as novidades do Projeto Base) para o seu fork no GitHub (origin).

### Envia a branch main local para o seu fork (origin)
`git push origin main`

# Dúvidas Específicas
## É possível atualizar meu repositório sem que apague todos meus arquivos?

Sim, é totalmente possível! O comando git merge upstream/main faz exatamente isso: ele combina os históricos. Seus arquivos e seus commits (F11, F12, F13, etc.) permanecem, e as novidades do upstream (P1, P2, etc.) são adicionadas. A única ressalva é que se houver conflitos, você terá que resolvê-los antes de finalizar a atualização.

Vamos fazer o fork por que queremos que toda atualização que fizermos no repositório modelo, queremos que todos integrantes do grupo de estudo sejam avisados.

O GitHub enviará a notificação para os watchers do Projeto Base. Como cada novo projeto é um fork separado, os integrantes do grupo podem:

Fazer watch (observar) o repositório Projeto Base original.

Ou, mais comum, usar o fluxo de trabalho acima, onde, ao iniciar o projeto, eles adicionam o Projeto Base como upstream e periodicamente o puxam para garantir que estão atualizados.

Portanto, o fork é a maneira correta de iniciar o projeto e a notificação é feita através do recurso Watch do GitHub. A atualização em si é feita localmente com git fetch e git merge.

Se tiverem muitos commits no seu fork e quiserem um histórico mais "limpo" (linear) da atualização, vocês podem usar git rebase em vez de git merge, mas para quem está começando, o git merge é mais seguro e mais fácil de reverter.

## O Erro no Comando (git pull origin upstream)
o comando correto para trazer as atualizações do repositório base (upstream) é feito em dois passos (ou um comando mais específico):

1. Busca (Fetch) e Fusão (Merge):
   `git fetch upstream
   git merge upstream/main # Ou upstream/master, dependendo do nome da branch`
2. Puxar (Pull):
`# O comando "git pull" é um atalho para "git fetch" + "git merge"
git pull upstream main`
   (Note que o comando seria upstream main e não origin upstream, pois origin e upstream são remotos diferentes).

## Alterações Locais Não Comitadas
O Cenário de Alterações Locais Não Comitadas
Se você tem alterações locais que não foram salvas com git add e git commit, o Git irá impedir o comando git pull ou git merge para proteger seu trabalho.

O que acontece (A Mensagem de Erro)
O Git vai interromper a operação e dar uma mensagem parecida com esta:

`error: Your local changes to the following files would be overwritten by merge:
caminho/do/seu/arquivo.txt
Please commit your changes or stash them before you merge.
Aborting`
Tradução: O Git percebeu que as mudanças que você está puxando do upstream afetam os mesmos arquivos que você modificou localmente. Ele não quer arriscar sobrescrever seu trabalho, então ele aborta a operação, deixando seu projeto exatamente como estava. Nenhum dado é perdido!

Como Resolver
Você tem duas opções principais quando o Git bloqueia o merge:

Opção	Ação	Quando Usar
1. Comitar as Alterações	Salve seu trabalho atual.	Se suas mudanças locais (FXX) são significativas e fazem parte da linha de desenvolvimento do seu projeto.
2. Usar git stash	Guarde suas alterações temporariamente.	Se suas mudanças locais são apenas um "rascunho" ou testes que você não quer comitar permanentemente agora.

Fluxo Usando git stash (Mais Comum para Atualizações)
Guardar (Stash): Salva suas alterações não comitadas em uma "pilha" temporária.
`git stash`

Atualizar: Agora que o diretório está limpo, puxe as novidades do Projeto Base.
`git pull upstream main`

Aplicar (Pop): Traz suas alterações de volta e tenta aplicá-las em cima das novidades.
`git stash pop`

Resumindo: O Git é muito cuidadoso com seu histórico e suas alterações. Ele sempre prefere dar uma mensagem de erro e abortar do que prosseguir e potencialmente apagar seu trabalho não salvo. Você está seguro!