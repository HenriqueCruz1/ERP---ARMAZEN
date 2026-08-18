from functions_usuarios import *

def menu():

    print("\n", '='*20)
    print('   SISTEMA DE ACESSO')
    print('='*20)
    print('1. Cadastrar novo usuário')
    print('2. Fazer login')
    print('3. Sair')
    return input('Escolha uma opção: ')

def iniciar():
    while True:

        opcao = menu()

        if opcao == '1':
            cadastrar()

        elif opcao == '2':
            logar()

        elif opcao == '3':
            print('Encerrando programa...')
            print(banco_de_usuarios)
            break
        
        else:
            print('Opção inválida. Tente novamente.')
iniciar()