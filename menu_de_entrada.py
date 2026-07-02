def menu():

    print("\n", '='*20)
    print('   SISTEMA DE ACESSO')
    print('='*20)
    print('1. Cadastrar novo usuário')
    print('2. Fazer login')
    print('3. Sair')
    return input('Escolha uma opção: ')

def cadastrar():

    while True:

        email = input('Digite o e-mail do novo usuário: ').strip()
    
        if email == '':
            print('Retorne uma resposta valida.')
            continue
    
        if '@' not in email:
            print('Retorne uma resposta valida.')
            continue
    
        if len(email) > 50:
            print('Retorne uma resposta valida.')
            continue

        break


    while True:

        senha = input('Digite a nova senha: ').strip()
    
        if senha == '':
            print('Retorne uma resposta valida.')
            continue
    
        if len(senha) > 10:
            print('Retorne uma resposta valida.')
            continue
    
        break

def login():
    print()


def iniciar():
    while True:

        opcao = menu()

        if opcao == '1':
            cadastrar()

        elif opcao == '2':
            login()

        elif opcao == '3':
            print('Encerrando programa...')
            break
        
        else:
            print('Opção inválida. Tente novamente.')
iniciar()



    











