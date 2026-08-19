from database import conectar

estoque = [
    {"nome": "Notebook", "preco": 3500, "quantidade": 8},
    {"nome": "Mouse", "preco": 80, "quantidade": 20}
]

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

def buscar_produto(estoque, nome):
        
        for produto in estoque:
            if produto['nome'].upper() == nome.upper():
                return produto

        return None

def cadastrar_produto(estoque):

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

    produto = {
          'nome': nome,
          'preco': preco,
          'quantidade': quantidade
     }

    estoque.append(produto)

def remover_produto(estoque):
     
    print('**REMOVER PRODUTO**\n')

    if not estoque:
        print('\nNão há nenhum item para ser removido. ')
        return
            

    encontrado = False
    while True: 
        nome = input('Qual produto deseja remover? ').upper()
        if nome == '':
            print('Este campo não pode ficar vazio.')
            continue
        break

    for produto in estoque:
        if produto['nome'].upper() == nome:
            encontrado = True
            estoque.remove(produto) 
            print('\nProduto removido com sucesso!')
            break

    if not encontrado:
        print('\nProduto não encontrado no estoque')

def editar_produto(estoque):

    print('**EDITAR PRODUTO**\n')

    while True:

        nome = input('Qual produto deseja editar? ')
        if nome =='':
            print('\nEste campo não pode ficar vazio.\n')
            continue
        break


    produto = buscar_produto(estoque, nome)

    if produto:

        print('Produto encontrado')
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

        produto['preco'] = novo_preco
        produto['quantidade'] = nova_quantidade

        print('Produto atualizado com sucesso!')

        listar_produtos(estoque)


