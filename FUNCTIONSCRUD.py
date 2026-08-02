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

    print('**BUSCAR PRODUTO**')
    
    for produto in estoque:
        if produto['nome'].upper() == nome:
            return produto
        
    return None


def cadastrar_produto(estoque):

    print('**CADASTRAR PRODUTO**')

    nome = input('Nome do produto: ')
    preco = float(input('Preço: '))
    quantidade = int(input('Quantidade: '))

    produto = {
          'nome': nome,
          'preco': preco,
          'quantidade': quantidade
     }

    estoque.append(produto)

def remover_produto(estoque):
     
    print('**REMOVER PRODUTO**')
     
    nome = input('Qual produto deseja remover? ').upper()
    for produto in estoque:
          if produto['nome'].upper() == nome:
            estoque.remove(produto) 
            print('Produto removido com sucesso!')
            break


def atualizar_produto(estoque):

    print('**ATUALIZAR PRODUTO**')

    buscar_produto()
