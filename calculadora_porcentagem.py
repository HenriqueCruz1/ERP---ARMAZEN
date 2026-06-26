def calculadora_desconto ():

    valor_desc = int(input('Insira o valor que recebera o desconto >;'))

    desconto = int(input('Quantos (%) de desconto deseja aplicar? '))

    regra_de_desconto = (100 - desconto) / 100
    calculo = valor_desc * regra_de_desconto
    
    return calculo


def calculadora_acrescimo():

    valor_acre = int(input('Insira o valor que recebera o acréscimo >;'))

    acrescimo = int(input('Quantos (%) de acréscimo deseja aplicar? '))

    regra_de_acrescimo = (100 + acrescimo) / 100

    calculo = valor_acre * regra_de_acrescimo

    return calculo


print(f'O valor atualizado com o desconto aplicado é: {calculadora_desconto()} R$')
print(f'O valor atualizado com o acréscimo aplicado é: {calculadora_acrescimo()} R$')


