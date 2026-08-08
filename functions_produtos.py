estoque = [
    {"nome": "Notebook", "preco": 3500, "quantidade": 8},
    {"nome": "Mouse", "preco": 80, "quantidade": 20}
]

def listar_produtos(estoque):

    print('**LISTAR PRODUTOS**')

    if not estoque:
        print('Não há informações para serem exibidas.')

    else:

        for produto in estoque:
            print(f'\nProduto: {produto['nome']}' )
            print(f'Preço: {produto['preco']}' )
            print(f'Quantidade: {produto['quantidade']}\n' )

def buscar_produto(estoque, nome):
    
    for produto in estoque:
        if produto['nome'].upper() == nome.upper():
            return produto
        
    print('Produto não encontrado!')
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
     
    print('**REMOVER PRODUTO**')

    encontrado = False
     
    nome = input('Qual produto deseja remover? ').upper()

    for produto in estoque:
        if produto['nome'].upper() == nome:
            encontrado = True
            estoque.remove(produto) 
            print('Produto removido com sucesso!')
            break

    if not encontrado:
        print('Produto não encontrado no estoque')

def editar_produto(estoque):

    print('**EDITAR PRODUTO**')

    nome = input('Qual produto deseja editar?')

    produto = buscar_produto(estoque, nome)

    if produto:

        print('Produto encontrado')

        novo_preco = float(input('Digite o novo preço: '))
        nova_quantidade = int(input('Digite a nova quantidade: '))

        produto['preco'] = novo_preco
        produto['quantidade'] = nova_quantidade

        print('Produto atualizado com sucesso!')

        listar_produtos(estoque)

    else:

        print('Produto não encontrado')

