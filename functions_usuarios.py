banco_de_usuarios = {
}


def cadastrar():

    while True:

        login = str(input('Digite o nome para o login do usuario: ')).strip()

        if login == '':
            print('Esté campo não pode ficar vazio.')
            continue

        if login in banco_de_usuarios:
            print('Esté nome de usúario não está disponivel.')
            continue

        if len(login) > 25 or len(login) < 3:
            print('Insira uma informação do tamanho adequado; entre 5 á 25 caracteres.')
            continue

        if '@' in login:
            print('O nome do usuario não pode ter caracteres especiais')
            continue 

        break

    while True:

        senha = str(input('Digite a nova senha: ')).strip()
    
        if senha == '':
            print('Esse campo não pode ficar vazio.')
            continue
    
        if len(senha) > 15 or len(senha) < 5 :
            print('Digite uma senha valida; a senha deve ter entre 5 á 15 caracteres.')
            continue
        
        banco_de_usuarios[login] = {'usuario': login,
                                    'senha': senha}

        break
    print('\n')
    print('** Novo usuário cadastrado com sucesso **') 

def logar():

    while True:

        login = input('Digite o Login: ').strip()

        if login not in banco_de_usuarios:
            print('Não há nenhum usuário cadastrado com esse login.')
            continue

        break

    while True:
        senha = input('Digite a senha. ').strip()

        if senha != banco_de_usuarios[login]['senha']:
            print('Senha incorreta.')
            continue
        else:

            break
    print('\n')
    print('++ Acesso permitido, SEJA BEM-VINDO! ++')




