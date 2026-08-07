from FUNCTIONSCRUD import *

def menu():

    while True:


        print('***MENU DE ENTRADA***\n')
        print('1 - listar produtos.\n'
        '2 - buscar produto.\n'
        '3 - cadastrar produtos.\n'
        '4 - remover produto. \n'
        '5 - atualizar produto.\n'
        '6 - sair')

        escolha_menu = int(input('Escolha uma opção: \n\n'))

        if escolha_menu == 1:
             listar_produtos(estoque)
        elif escolha_menu == 2:
             nome = input('Qual produto quer buscar? ')
             buscar_produto(estoque, nome)
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
