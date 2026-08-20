from database import conectar
# Importa a função conectar, responsável por estabelecer a conexão com o banco.

def buscar_produto(nome):
    # Define uma função que recebe o nome de um produto para realizar a busca.

    conexao = conectar()
    # Armazena a conexão retornada pela função conectar.

    cursor = conexao.cursor()
    # Cria um cursor, utilizado para executar comandos SQL e obter seus resultados.

    cursor.execute(
        """
        SELECT nome, preco, quantidade
        FROM produtos
        WHERE UPPER(nome) = UPPER(%s)
        """,
        (nome,))
        # Compara o nome armazenado no banco com o nome recebido pela função,
        # ignorando diferenças entre letras maiúsculas e minúsculas.
        # Define a tabela produtos como origem dos dados.
        # Seleciona as colunas nome, preco e quantidade.
        # Fornece o valor que será utilizado no lugar do placeholder %s.
    

    produto = cursor.fetchone()
    # Obtém o primeiro registro encontrado pela consulta e armazena em produto.

    cursor.close()
    # Fecha o cursor após a execução da consulta.

    conexao.close()
    # Fecha a conexão com o banco de dados.

    return produto
    # Retorna o produto encontrado pela função.


produto = buscar_produto("notebook")
# Chama a função buscar_produto passando "notebook" como argumento.

print(produto)
# Exibe na tela o resultado retornado pela função.





