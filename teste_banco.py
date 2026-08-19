from database import conectar

def buscar_produto(nome):

    conexao = conectar() # criar uma variavel que leva o valor da função

    cursor = conexao.cursor() #cria o o objeto que executa SQL

    cursor.execute(
        """
        SELECT nome, preco, quantidade 
        FROM produtos
        WHERE UPPER(nome) = UPPER(%s)
        """, 
        (nome,)
    ) #Comando para o python executar a busca no BD SQL

    produto = cursor.fetchone() #Ele pega as informações que foram pegas pelo .execute

    cursor.close()
    conexao.close()

    return produto

produto = buscar_produto("notebook")

print(produto)


