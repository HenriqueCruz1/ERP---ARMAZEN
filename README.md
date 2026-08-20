**Definição do que é?

Projeto inicialmente para estudos mas com possibilidade de crescer e virar uma aplicação real a longo prazo;

**Sobre a aplicação:

Estrutura baseada em um ERP, o foco no momento é criar a estrutura de estoque [12/08/2026]

Documentação do processo de criação na tela de login.

Organize oque terá no seu menu de entrada.

- input de login

------------------------
        login
------------------------

- input de senha

------------------------
        senha
------------------------

faça as camadas de proteção.

--- para não confundir eu criei funções distintas def verifica_senha, def verifica_email --- 

Especificação de camadas teste // Projetando arquitetura de filtros. 

1° proteção de borda - failfast (nulos, vazios, espaços)

2° proteção de negocio(contém arroba, se é maior que 50)

3° permitir acesso ao core da aplicação (até que os dados estiverem seguros)

Modelagem de dados:

+ O cadastro do úsuario, acesso e validação básica, foram implementados.

++ Estou estudando formas de validação com hash e JWT.

++ estou fazendo o sistema de movimentação interna de saldo com um CRUD

+ Quando a função busca uma informação no laço e retorna um valor sobre uma variavel use return, ela já vai encerrar a função caso encontre ou não a informação e entregar o valor final.

+ Quando a função só executa uma tarefa dentro do sistema (exp: atualiza ou remove um dado) use uma condicional true/false para a execução da ação.

Teste de funções CRUD

** Cadastro
nome vazio - Ok
preço inválido - Ok
preço negativo - Ok
quantidade inválida - Ok
quantidade negativa - Ok

** Busca
produto existente - Ok
produto inexistente - Ok
maiúsculas/minúsculas - Ok
entrada vazia - Ok

** Edição
produto existente - Ok
produto inexistente - Ok
preço/quantidade inválidos - Ok
entrada vazia - Ok

** Remoção
existente - Ok
inexistente - Ok
estoque vazio - OK
entrada vazia - Ok

** Listagem
estoque com produtos - Ok
estoque vazio - Ok

** Menu
opção válida - Ok
opção inexistente - Ok
entrada que não seja número - Ok
entrada vazia - Ok

** PostgreSQL

Acessar postgre pelo terminal: sudo -u postgres psql

CREATE DATABASE erp; - (criei um banco de dados chamado erp)

- acesse o banco usando \c erp no terminal enquanto estiver conectado ao psql
- vamos criar nossa primeira tabela, o psql não vai aceitar se ela estiver vazia, então o passo a passo segue:

+ CREATE TABLE produtos (
        nome VARCHAR(100) (no terminal são 4 espaços ou nenhum)
);

++ Criamos a tabela 'produtos' que recebe uma coluna chamada nome, que em cada linha podem ser escritos até 100 caracteres.
+++ Visualize a tabela com o comando \dt

** INSERINDO VALORES A TABELA
Vamos inserir um produto na ta tabela;

INSERT INTO produtos (nome)
VALUES ('Notebook) no terminal se pode escrever tudo em uma linha só que o sistema aceita.

** INSERINDO UMA NOVA COLUNA.
vamos inserir uma nova coluna na tabela;
comando: ALTER TABLE produtos ADD preco NUMERIC(100)

- Codificando o sistema de usuarios.

- Divisão do menu e suas funções cada um em seu arquivo.

-- Iniciando frontend para começar testes --

- Finalizar a integração com o SQl
* Vamos usar o psycopg3 - é uma biblioteca qu conversa com o postgre
pip install psycopg

Arquivos futuros:

produtos.py
clientes.py
vendas.py
estoque.py
fornecedores.py
database.py - responsavel pela conexão

defina a senha do SQL pelo terminal:
\password postgres
Informações da porta do banco de dados:
\conninfo

Tasks of day

** Alterar as funções trocando o banco de dados para SQL **

+ Listar produtos (Ok)
+ Buscar produto (Ok)
+ Cadastrar produto (Ok)
+ Remover produto (Ok)
+ Editar produto (Ok)

## Deixar tudo comentado

** Iniciar frontend - Html, css, javascript.













