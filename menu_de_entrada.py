def verifica_email(email):

    email = input()

    # Proteção de borda

    if email == None:
        return False
    
    if email == '':
        return False
    
print(verifica_email)
    
def verifica_senha(senha):

    senha = input()

    if senha == None:
        return False
    
    if senha == '':
        return False

print(verifica_senha)


  #   Proteção de négocio


#leia a string, verifique a existencia de um caractere especifico. 

print(15*'-', 'EMAIL//LOGIN* ')

verifica_email()

print(15*'-', 'SENHA//LOGIN* ')

verifica_senha()
    











