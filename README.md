Definição do que é?

DEFINIÇÃO:

Sistema de gestão que faz a intregração de inicialmente 3 modulos:

 => ESTOQUE
 => COMPRAS
 => FINANCEIRO  

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

++ Task's of the day

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

