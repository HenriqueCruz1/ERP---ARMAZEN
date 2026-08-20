from app.database import conectar

def listar_produtos():

    print('**LISTAR PRODUTOS**')

    conexao = conectar()
    cursor = conexao.cursor()

    cursor. execute ("SELECT nome, preco, quantidade FROM produtos")

    produtos = cursor.fetchall()

    if not produtos:
        print('Não há informações para serem exibidas.')

    else:

        for produto in produtos:
            print(f'\nProduto: {produto[0]}' )
            print(f'Preço: {produto[1]}' )
            print(f'Quantidade: {produto[2]}\n' )

    cursor.close()
    conexao.close()


def buscar_produto(nome):

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """SELECT nome, preco, quantidade
        FROM produtos
        WHERE UPPER(nome) = UPPER(%s)
        """,
        (nome,)
    )
    produto = cursor.fetchone()

    cursor.close()
    conexao.close()

    return produto

def inserir_produto(nome, preco,quantidade):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute (
        """INSERT INTO produtos (nome, preco, quantidade)
    VALUES(%s,%s,%s)""",
    (nome, preco,quantidade)
)
    conexao.commit()
    
    cursor.close()
    conexao.close()

def cadastrar_produto():

    print('\n**CADASTRAR PRODUTO**\n')

    while True:
        nome = input('Nome do produto: ')
        if nome == '':
            print('Este campo não pode ficar vazio')
            continue
        break
    while True:
        try:
            preco = float(input('Preço: '))
            if preco < 0:
                print('O valor não pode ser negativo!')
                continue
            break
        except ValueError:
            print('Entrada invalida')
    while True:
        try:
            quantidade = int(input('Quantidade: '))
            if quantidade < 0:
                print('O valor não pode ser negativo')
                continue
            break
        except ValueError:
            print('Valor invalido')

    inserir_produto(nome, preco, quantidade)

    print("\nProduto cadastrado com sucesso!")

def deletar_produto(nome):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""DELETE FROM produtos
    WHERE UPPER(nome) = UPPER(%s)""",
    (nome,)
)
    conexao.commit()

    cursor.close()
    conexao.close()

def remover_produto():
    print('**REMOVER PRODUTO**\n')

    while True: 
        nome = input('Qual produto deseja remover? ').upper()

        if nome == '':
            print('Este campo não pode ficar vazio.')
            continue

        break

    produto = buscar_produto(nome)

    if not produto:
        print('\nProduto não encontrado no estoque.')
        return

    deletar_produto(nome)

    print("\nProduto removido com sucesso!")

def atuallizar_produto(nome, novo_preco, nova_quantidade):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """UPDATE produtos
        SET preco = %s, 
            quantidade = %s
        WHERE UPPER(nome) = UPPER(%s)""",
        (novo_preco, nova_quantidade, nome)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

def editar_produto():

    print('**EDITAR PRODUTO**\n')

    while True:

        nome = input('Qual produto deseja editar? ')
        if nome =='':
            print('\nEste campo não pode ficar vazio.\n')
            continue
        break


    produto = buscar_produto(nome)

    if not produto:
        print("\nProduto não encontrado")
        return
    
    print('Produto encontrado!\n')

    while True:
        try:
            novo_preco = float(input('Digite o novo preço: '))

            if novo_preco < 0:
                print('O valor não pode ser negativo!')
                continue

            break
        except ValueError:
            print('Entrada invalida')

    while True:
        try:    
            nova_quantidade = int(input('Digite a nova quantidade: '))

            if nova_quantidade < 0:
                print('O valor não pode ser negativo')
                continue

            break

        except ValueError:
                print('Entrada invalida!')

    atuallizar_produto(nome, novo_preco, nova_quantidade)

    print('Produto atualizado com sucesso!')

    listar_produtos()


