from usuarios.functions_usuarios import AuthCLI
from produtos.menu_produtos import EstoqueCLI
from produtos.functions_produtosPOO import EstoqueService


def main():
    auth = AuthCLI()
    usuario = auth.executar()

    if usuario is None:
        return

    service = EstoqueService(usuario_id=usuario.id)
    estoque = EstoqueCLI(service=service)
    estoque.executar()

if __name__ == "__main__":
    main()
    