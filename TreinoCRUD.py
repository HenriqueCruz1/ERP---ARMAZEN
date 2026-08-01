estoque = [
    {"nome": "Notebook", "preco": 3500, "quantidade": 8},
    {"nome": "Mouse", "preco": 80, "quantidade": 20}
]

def listar_produtos(estoque):
    for produto in estoque:
        print(f'\nProduto: {produto['nome']}' )
        print(f'Preço: {produto['preco']}' )
        print(f'Quantidade: {produto['quantidade']}\n' )

listar_produtos(estoque)


def buscar_produto(estoque, nome):
    
    for produto in estoque:
        if produto['nome'].upper() == nome:
            return produto
        
    return None

nome = input('Digite o nome do produto: ').upper()        
resultado = buscar_produto(estoque, nome)

if resultado:
    print(f'Produto: {resultado['nome']}')
    print(f'Preço: {resultado['preco']}')
    print(f'Quantidade: {resultado['quantidade']}')
else:
        print('Produto não encontrado')

def cadastrar_produto(estoque):

    nome = input('Nome do produto: ')
    preco = float(input('Preço: '))
    quantidade = int(input('Quantidade: '))

    produto = {
          'nome': nome,
          'preco': preco,
          'quantidade': quantidade
     }

    estoque.append(produto)

cadastrar_produto(estoque)
listar_produtos(estoque)

def remover_produto(estoque):
     nome = input('Qual produto deseja remover? ').upper()
     for produto in estoque:
          if produto['nome'].upper() == nome:
            estoque.remove(produto) 
            print('Produto removido com sucesso!')
            break

remover_produto(estoque)
listar_produtos(estoque)










