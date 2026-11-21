from contextlib import contextmanager
from dataclasses import dataclass

from database import conectar


# ---------------------------------------------------------------------------
# ENTIDADE
# ---------------------------------------------------------------------------
@dataclass
class Produto:
    """Representa um produto do estoque e valida seus próprios dados."""

    nome: str
    preco: float
    quantidade: int
    id: int = None

    def __post_init__(self):
        self.nome = (self.nome or "").strip()
        if not self.nome:
            raise ValueError("O nome não pode ficar vazio.")
        if self.preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        if self.quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

    def __str__(self):
        return (
            f"\nProduto: {self.nome}"
            f"\nPreço: R$ {self.preco:.2f}"
            f"\nQuantidade: {self.quantidade}\n"
        )


# ---------------------------------------------------------------------------
# ACESSO A DADOS (só fala com o banco)
# ---------------------------------------------------------------------------
class ProdutoRepository:
    """Responsável exclusivamente pelas operações SQL."""

    @contextmanager
    def _cursor(self, commit=False):
        """Abre conexão/cursor e garante commit, rollback e fechamento."""
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

    def listar(self, usuario_id):
        with self._cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, preco, quantidade
                FROM produtos
                WHERE usuario_id = %s
                ORDER BY nome
                """,
                (usuario_id,)
            )
    
            linhas = cursor.fetchall()
    
            return [
                Produto(
                    nome=n,
                    preco=float(p),
                    quantidade=q,
                    id=i
                )
                for i, n, p, q in linhas
            ]

    def buscar(self, nome, usuario_id):
        with self._cursor() as cursor:
            cursor.execute(
            """
            SELECT nome, preco, quantidade
            FROM produtos
            WHERE UPPER(nome) = UPPER(%s)
            AND usuario_id = %s
            """,
            (nome, usuario_id),
        )
            linha = cursor.fetchone()

            return Produto(linha[0], float(linha[1]), linha[2]) if linha else None

    def buscar_por_id(self, produto_id, usuario_id):
        with self._cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, preco, quantidade
                FROM produtos
                WHERE id = %s
                AND usuario_id = %s
                """,
                (produto_id, usuario_id),
            )

            linha = cursor.fetchone()

            if linha is None:
                return None

            return Produto(
                id=linha[0],
                nome=linha[1],
                preco=float(linha[2]),
                quantidade=linha[3]
            )

    def inserir(self, produto, usuario_id):
        with self._cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO produtos (nome, preco, quantidade, usuario_id)
                VALUES (%s, %s, %s, %s)
                """,
                (produto.nome, produto.preco, produto.quantidade, usuario_id),
            )

    def atualizar(self, produto, produto_id, usuario_id):
        with self._cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE produtos
                SET preco = %s, quantidade = %s
                WHERE id = %s
                AND usuario_id = %s
                """,
                (produto.preco, produto.quantidade, produto_id, usuario_id),
            )
            return cursor.rowcount > 0

    def deletar(self, nome, usuario_id):
        with self._cursor(commit=True) as cursor:
            cursor.execute(
            """
            DELETE FROM produtos
            WHERE UPPER(nome) = UPPER(%s)
            AND usuario_id = %s
            """,
            (nome, usuario_id),
        )
        return cursor.rowcount > 0

    def deletar_por_id(self, produto_id, usuario_id):
        with self._cursor(commit=True) as cursor:
            cursor.execute(
                """
                DELETE FROM produtos
                WHERE id = %s
                AND usuario_id = %s
                """,
                (produto_id, usuario_id),
            )

            return cursor.rowcount > 0


# ---------------------------------------------------------------------------
# REGRAS DE NEGÓCIO
# ---------------------------------------------------------------------------
class EstoqueService:
    """Regras do estoque, sem print/input."""

    def __init__(self, usuario_id, repository=None):
        self.usuario_id = usuario_id
        self.repository = repository or ProdutoRepository()

    def listar(self):
        return self.repository.listar(self.usuario_id)

    def cadastrar(self, nome, preco, quantidade):
        produto = Produto(nome, preco, quantidade)  # valida aqui
        if self.repository.buscar(produto.nome, self.usuario_id):
            raise ValueError("Já existe um produto com esse nome.")
        self.repository.inserir(produto, self.usuario_id)

    def editar(self, produto_id, novo_preco, nova_quantidade):
        produto = self.repository.buscar_por_id(
            produto_id,
            self.usuario_id
        )
    
        if not produto:
            raise LookupError("Produto não encontrado no estoque.")
    
        produto_atualizado = Produto(
            nome=produto.nome,
            preco=novo_preco,
            quantidade=nova_quantidade
        )
    
        self.repository.atualizar(
            produto_atualizado,
            produto_id,
            self.usuario_id
        )

    def remover(self, nome):
        if not self.repository.deletar(nome, self.usuario_id):
            raise LookupError("Produto não encontrado no estoque.")

    def existe(self, nome):
        return self.repository.buscar(nome, self.usuario_id) is not None

    def remover_por_id(self, produto_id):
        if not self.repository.deletar_por_id(produto_id, self.usuario_id):
            raise LookupError("Produto não encontrado no estoque.")




    