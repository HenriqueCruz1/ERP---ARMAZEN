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
             listar_produtos()
        elif escolha_menu == 2:
          print('**BUSCAR PRODUTO**\n')

          nome = input('Qual produto quer buscar? ')
          if nome =='':
               print('Este campo não pode ficar vazio')

          produto = buscar_produto(nome)

          if produto:
            print(f"\nProduto: {produto[0]}")
            print(f"Preço: {produto[1]}")
            print(f"Quantidade: {produto[2]}\n")
          else:
            print('Produto não encontrado.')
            
        elif escolha_menu == 3:
             cadastrar_produto()
        elif escolha_menu == 4:
             remover_produto()
        elif escolha_menu == 5:
               editar_produto()
        elif escolha_menu == 6:
            print('Saindo..')
            break
            
menu()
