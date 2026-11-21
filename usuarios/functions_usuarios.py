import hashlib
import hmac
import re
import secrets
from contextlib import contextmanager
from dataclasses import dataclass
from getpass import getpass
from typing import Optional

import psycopg
from psycopg.errors import UniqueViolation

from database import conectar  # o mesmo módulo usado no sistema de estoque


# ---------------------------------------------------------------------------
# EXCEÇÕES DO DOMÍNIO
# ---------------------------------------------------------------------------
class ValidacaoError(ValueError):
    """Dados informados fora das regras (login/senha inválidos)."""


class LoginJaExisteError(Exception):
    """Já existe um usuário com esse login."""


class CredenciaisInvalidasError(Exception):
    """Login ou senha incorretos (mensagem propositalmente genérica)."""


# ---------------------------------------------------------------------------
# SEGURANÇA: hash de senha (nunca guardar senha em texto puro)
# ---------------------------------------------------------------------------
class PasswordHasher:
    """PBKDF2-HMAC-SHA256 com salt aleatório. Formato: algoritmo$iter$salt$hash."""

    ALGORITMO = "pbkdf2_sha256"
    ITERACOES = 600_000

    def gerar(self, senha: str) -> str:
        salt = secrets.token_hex(16)
        digest = self._derivar(senha, salt, self.ITERACOES)
        return f"{self.ALGORITMO}${self.ITERACOES}${salt}${digest}"

    def verificar(self, senha: str, senha_hash: str) -> bool:
        try:
            _, iteracoes, salt, digest = senha_hash.split("$")
            esperado = self._derivar(senha, salt, int(iteracoes))
        except ValueError:
            return False
        return hmac.compare_digest(esperado, digest)  # tempo constante

    @staticmethod
    def _derivar(senha: str, salt: str, iteracoes: int) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256", senha.encode(), salt.encode(), iteracoes
        ).hex()


# ---------------------------------------------------------------------------
# ENTIDADE
# ---------------------------------------------------------------------------
@dataclass
class Usuario:
    login: str
    senha_hash: str
    id: Optional[int] = None

    LOGIN_MIN, LOGIN_MAX = 3, 25
    SENHA_MIN, SENHA_MAX = 5, 15
    _PADRAO_LOGIN = re.compile(r"^[A-Za-z0-9_]+$")

    @classmethod
    def validar_login(cls, login: str) -> str:
        login = (login or "").strip()
        if not login:
            raise ValidacaoError("Este campo não pode ficar vazio.")
        if not cls.LOGIN_MIN <= len(login) <= cls.LOGIN_MAX:
            raise ValidacaoError(
                f"O login deve ter entre {cls.LOGIN_MIN} e {cls.LOGIN_MAX} caracteres."
            )
        if not cls._PADRAO_LOGIN.match(login):
            raise ValidacaoError(
                "O login só pode conter letras, números e underscore (_)."
            )
        return login

    @classmethod
    def validar_senha(cls, senha: str) -> str:
        if not senha:
            raise ValidacaoError("Este campo não pode ficar vazio.")
        if not cls.SENHA_MIN <= len(senha) <= cls.SENHA_MAX:
            raise ValidacaoError(
                f"A senha deve ter entre {cls.SENHA_MIN} e {cls.SENHA_MAX} caracteres."
            )
        return senha


# ---------------------------------------------------------------------------
# ACESSO A DADOS (só SQL)
# ---------------------------------------------------------------------------
class UsuarioRepository:
    @contextmanager
    def _cursor(self, commit=False):
        conexao = conectar()
        try:
            cursor = conexao.cursor()
            try:
                yield cursor
                if commit:
                    conexao.commit()
            except Exception:
                conexao.rollback()
                raise
            finally:
                cursor.close()
        finally:
            conexao.close()

    def criar_tabela(self):
        """Cria a tabela e o índice único (login sem diferenciar maiúsculas)."""
        with self._cursor(commit=True) as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS usuarios (
                       id         SERIAL PRIMARY KEY,
                       login      VARCHAR(25) NOT NULL,
                       senha_hash TEXT        NOT NULL,
                       criado_em  TIMESTAMP   NOT NULL DEFAULT NOW()
                   )"""
            )
            cursor.execute(
                """CREATE UNIQUE INDEX IF NOT EXISTS usuarios_login_unico
                   ON usuarios (LOWER(login))"""
            )

    def buscar_por_login(self, login: str) -> Optional[Usuario]:
        with self._cursor() as cursor:
            cursor.execute(
                """SELECT id, login, senha_hash
                   FROM usuarios
                   WHERE LOWER(login) = LOWER(%s)""",
                (login,),
            )
            linha = cursor.fetchone()
        return Usuario(id=linha[0], login=linha[1], senha_hash=linha[2]) if linha else None

    def inserir(self, usuario: Usuario) -> None:
        try:
            with self._cursor(commit=True) as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (login, senha_hash) VALUES (%s, %s)",
                    (usuario.login, usuario.senha_hash),
                )
        except psycopg.errors.UniqueViolation:
            # a garantia final de unicidade é do banco (evita condição de corrida)
            raise LoginJaExisteError("Este nome de usuário não está disponível.")


# ---------------------------------------------------------------------------
# REGRAS DE NEGÓCIO
# ---------------------------------------------------------------------------
class AuthService:
    def __init__(self, repository=None, hasher=None):
        self.repository = repository or UsuarioRepository()
        self.hasher = hasher or PasswordHasher()
        # hash "falso" para gastar o mesmo tempo quando o login não existe
        self._hash_falso = self.hasher.gerar("senha-falsa")

    def login_disponivel(self, login: str) -> bool:
        return self.repository.buscar_por_login(login) is None

    def cadastrar(self, login: str, senha: str) -> Usuario:
        login = Usuario.validar_login(login)
        senha = Usuario.validar_senha(senha)
        if not self.login_disponivel(login):
            raise LoginJaExisteError("Este nome de usuário não está disponível.")
        usuario = Usuario(login=login, senha_hash=self.hasher.gerar(senha))
        self.repository.inserir(usuario)
        return usuario

    def autenticar(self, login: str, senha: str) -> Usuario:
        usuario = self.repository.buscar_por_login((login or "").strip())
        if usuario is None:
            self.hasher.verificar(senha, self._hash_falso)
            raise CredenciaisInvalidasError("Login ou senha incorretos.")
        if not self.hasher.verificar(senha, usuario.senha_hash):
            raise CredenciaisInvalidasError("Login ou senha incorretos.")
        return usuario


# ---------------------------------------------------------------------------
# INTERFACE (só print/input)
# ---------------------------------------------------------------------------
class AuthCLI:
    MAX_TENTATIVAS = 3

    def __init__(self, service=None):
        self.service = service or AuthService()

    def cadastrar(self):
        print("\n**CADASTRAR USUÁRIO**\n")

        while True:
            login = input("Digite o nome para o login do usuário: ")
            try:
                login = Usuario.validar_login(login)
                if not self.service.login_disponivel(login):
                    print("Este nome de usuário não está disponível.")
                    continue
                break
            except ValidacaoError as erro:
                print(erro)

        while True:
            senha = getpass("Digite a nova senha: ")
            try:
                Usuario.validar_senha(senha)
            except ValidacaoError as erro:
                print(erro)
                continue
            if senha != getpass("Confirme a senha: "):
                print("As senhas não conferem.")
                continue
            break

        try:
            self.service.cadastrar(login, senha)
            print("\n** Novo usuário cadastrado com sucesso **")
        except (ValidacaoError, LoginJaExisteError) as erro:
            print(f"\n{erro}")

    def logar(self):
        print("\n**LOGIN**\n")

        for tentativa in range(1, self.MAX_TENTATIVAS + 1):
            login = input("Digite o login: ").strip()
            senha = getpass("Digite a senha: ")
            try:
                usuario = self.service.autenticar(login, senha)
            except CredenciaisInvalidasError as erro:
                restantes = self.MAX_TENTATIVAS - tentativa
                print(f"{erro} Tentativas restantes: {restantes}\n")
                continue
            print(f"\n++ Acesso permitido, SEJA BEM-VINDO, {usuario.login}! ++")
            return usuario

        print("Número máximo de tentativas excedido.")
        return None

    def executar(self):
        while True:
            print("\n**USUÁRIOS**")
            print("1 - Cadastrar")
            print("2 - Logar")
            print("0 - Sair")
    
            escolha = input("Escolha: ").strip()
    
            if escolha == "0":
                print("Até logo!")
                return None
    
            elif escolha == "1":
                self.cadastrar()
    
            elif escolha == "2":
                usuario = self.logar()
    
                if usuario is not None:
                    return usuario
    
            else:
                print("Opção inválida.")


if __name__ == "__main__":
    UsuarioRepository().criar_tabela()
    AuthCLI().executar()