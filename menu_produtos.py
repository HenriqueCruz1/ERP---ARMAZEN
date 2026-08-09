from functions_produtos import *

def menu():

    while True:
        try:


          print('\n***MENU DE ENTRADA***\n')
          print('1 - listar produtos.\n'
          '2 - buscar produto.\n'
          '3 - cadastrar produtos.\n'
          '4 - remover produto. \n'
          '5 - editar produto.\n'
          '6 - sair\n')

     
          escolha_menu = int(input('Escolha uma opção: '))
          if escolha_menu <= 0 or escolha_menu >= 7:
               print('Digite uma opção valida.')
               continue
        except ValueError:
             print('Entrada invalida.')
             continue

        if escolha_menu == 1:
             listar_produtos(estoque)
        elif escolha_menu == 2:
               print('**BUSCAR PRODUTO**\n')
               
               while True:

                    nome = input('Qual produto quer buscar? ')
                    if nome =='':
                         print('Este campo não pode ficar vazio')
                         continue
                    break

               produto = buscar_produto(estoque, nome)

               if produto:
                    print(f"\nProduto: {produto['nome']}")
                    print(f"Preço: {produto['preco']}")
                    print(f"Quantidade: {produto['quantidade']}\n")

        elif escolha_menu == 3:
             cadastrar_produto(estoque)
        elif escolha_menu == 4:
             remover_produto(estoque)
        elif escolha_menu == 5:
            editar_produto(estoque)
        elif escolha_menu == 6:
            print('Saindo..')
            break
            
menu()
