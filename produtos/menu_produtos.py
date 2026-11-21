from produtos.functions_produtosPOO import *

# ---------------------------------------------------------------------------
# INTERFACE (só print/input)
# ---------------------------------------------------------------------------
class EstoqueCLI:
    def __init__(self, service=None):
        self.service = service or EstoqueService()

    # ----- helpers de entrada (acabam com a repetição de while/try) -----
    @staticmethod
    def _ler_texto(mensagem):
        while True:
            valor = input(mensagem).strip()
            if valor:
                return valor
            print("Este campo não pode ficar vazio.")

    @staticmethod
    def _ler_numero(mensagem, tipo):
        while True:
            try:
                valor = tipo(input(mensagem))
            except ValueError:
                print("Entrada inválida.")
                continue
            if valor < 0:
                print("O valor não pode ser negativo!")
                continue
            return valor

    # ----- ações do menu -----
    def listar(self):
        print("\n**LISTAR PRODUTOS**")
        produtos = self.service.listar()
        if not produtos:
            print("Não há informações para serem exibidas.")
            return
        for produto in produtos:
            print(produto)

    def cadastrar(self):
        print("\n**CADASTRAR PRODUTO**\n")
        nome = self._ler_texto("Nome do produto: ")
        preco = self._ler_numero("Preço: ", float)
        quantidade = self._ler_numero("Quantidade: ", int)
        try:
            self.service.cadastrar(nome, preco, quantidade)
            print("\nProduto cadastrado com sucesso!")
        except ValueError as erro:
            print(f"\n{erro}")

    def editar(self):
        print("\n**EDITAR PRODUTO**\n")
        nome = self._ler_texto("Qual produto deseja editar? ")
        if not self.service.existe(nome):
            print("\nProduto não encontrado.")
            return
        print("Produto encontrado!\n")
        novo_preco = self._ler_numero("Digite o novo preço: ", float)
        nova_quantidade = self._ler_numero("Digite a nova quantidade: ", int)
        try:
            self.service.editar(nome, novo_preco, nova_quantidade)
            print("\nProduto atualizado com sucesso!")
            self.listar()
        except (ValueError, LookupError) as erro:
            print(f"\n{erro}")

    def remover(self):
        print("\n**REMOVER PRODUTO**\n")
        nome = self._ler_texto("Qual produto deseja remover? ")
        try:
            self.service.remover(nome)
            print("\nProduto removido com sucesso!")
        except LookupError as erro:
            print(f"\n{erro}")

    def executar(self):
        opcoes = {
            "1": ("Listar produtos", self.listar),
            "2": ("Cadastrar produto", self.cadastrar),
            "3": ("Editar produto", self.editar),
            "4": ("Remover produto", self.remover),
        }
        while True:
            print("\n**ESTOQUE**")
            for chave, (titulo, _) in opcoes.items():
                print(f"{chave} - {titulo}")
            print("0 - Sair")

            escolha = input("Escolha: ").strip()
            if escolha == "0":
                print("Até logo!")
                break
            if escolha in opcoes:
                opcoes[escolha][1]()
            else:
                print("Opção inválida.")


if __name__ == "__main__":
     EstoqueCLI().executar()