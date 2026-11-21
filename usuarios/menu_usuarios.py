from typing import Callable, List, Optional, Tuple

import psycopg
from psycopg.errors import UniqueViolation

from usuarios.functions_usuarios import AuthCLI, Usuario, UsuarioRepository

Acao = Callable[[], None]


# ---------------------------------------------------------------------------
# MENU GENÉRICO (reutilizável: serve para o acesso, para o estoque, etc.)
# ---------------------------------------------------------------------------
class Menu:
    """Menu numerado automaticamente; a última opção é sempre 'sair'."""

    def __init__(
        self,
        titulo: str,
        opcoes: List[Tuple[str, Acao]],
        rotulo_saida: str = "Sair",
        largura: int = 20,
    ):
        self.titulo = titulo
        self.opcoes = opcoes
        self.rotulo_saida = rotulo_saida
        self.largura = max(largura, len(titulo) + 4)

    @property
    def _codigo_saida(self) -> str:
        return str(len(self.opcoes) + 1)

    def exibir(self) -> None:
        print("\n" + "=" * self.largura)
        print(self.titulo.center(self.largura))
        print("=" * self.largura)
        for numero, (rotulo, _) in enumerate(self.opcoes, start=1):
            print(f"{numero}. {rotulo}")
        print(f"{self._codigo_saida}. {self.rotulo_saida}")

    def executar(self) -> None:
        """Mostra o menu em loop até o usuário escolher sair."""
        while True:
            self.exibir()
            try:
                escolha = input("Escolha uma opção: ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                escolha = self._codigo_saida  # Ctrl+C / Ctrl+D = sair

            if escolha == self._codigo_saida:
                print("Encerrando programa...")
                return

            if escolha.isdigit() and 1 <= int(escolha) <= len(self.opcoes):
                _, acao = self.opcoes[int(escolha) - 1]
                acao()
            else:
                print("Opção inválida. Tente novamente.")


# ---------------------------------------------------------------------------
# APLICAÇÃO
# ---------------------------------------------------------------------------
class SistemaAcesso:
    """Liga o menu às ações de cadastro/login e guarda quem está logado."""

    def __init__(
        self,
        auth_cli: Optional[AuthCLI] = None,
        repository: Optional[UsuarioRepository] = None,
        ao_logar: Optional[Callable[[Usuario], None]] = None,
    ):
        self.auth = auth_cli or AuthCLI()
        self.repository = repository or UsuarioRepository()
        self.ao_logar = ao_logar  # o que fazer após um login bem-sucedido
        self.usuario_logado: Optional[Usuario] = None

        self.menu = Menu(
            "SISTEMA DE ACESSO",
            [
                ("Cadastrar novo usuário", self._proteger(self.auth.cadastrar)),
                ("Fazer login", self._proteger(self._logar)),
            ],
        )

    @staticmethod
    def _proteger(acao: Acao) -> Acao:
        """Evita que uma falha de banco derrube o programa inteiro."""

        def executar():
            try:
                acao()
            except psycopg.Error:
                print("\nErro ao acessar o banco de dados. Tente novamente.")

        return executar

    def _logar(self) -> None:
        usuario = self.auth.logar()
        if usuario is None:
            return
        self.usuario_logado = usuario
        if self.ao_logar:
            self.ao_logar(usuario)

    def iniciar(self) -> None:
        try:
            self.repository.criar_tabela()
        except psycopg.Error:
            print("Não foi possível conectar ao banco de dados. Encerrando.")
            return
        self.menu.executar()


if __name__ == "__main__":
    SistemaAcesso().iniciar()