def verifica_email(email):

    if email is None:
        return False
    
    if email == '':
        return False
    
    if '@' not in email:
        return False
    
    if len(email) > 50:
        return False

    
def verifica_senha(senha):

    if senha is None:
        return False
    
    if senha == '':
        return False
    
    if '@' not in senha:
        return False
    
    if len(senha) > 50:
        return False



print(15*'-', 'EMAIL//LOGIN* ')

print(verifica_email(email = input('Digite o e-mail: ')))

print(15*'-', 'SENHA//LOGIN* ')

print(verifica_senha(senha = input('Digite a senha: ')))

    











