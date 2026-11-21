
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from usuarios.functions_usuarios import AuthService, CredenciaisInvalidasError
from produtos.functions_produtosPOO import EstoqueService

app = Flask(__name__)

app.config["SECRET_KEY"] = "chave-temporaria-para-desenvolvimento"

auth_service = AuthService()


@app.route("/")
def inicio():
    if "usuario_id" not in session:
        return redirect(url_for("pagina_login"))

    return render_template("produtos.html")


@app.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == "GET":
        return render_template("login.html")

    dados = request.get_json()

    login = dados.get("login", "")
    senha = dados.get("senha", "")

    try:
        usuario = auth_service.autenticar(login, senha)

        session.clear()
        session["usuario_id"] = usuario.id

        return jsonify({
            "mensagem": "Login realizado com sucesso!"
        }), 200

    except CredenciaisInvalidasError:
        return jsonify({
            "erro": "Login ou senha incorretos."
        }), 401


@app.route("/produtos", methods=["GET", "POST"])
def listar_produtos():
    if "usuario_id" not in session:
        return jsonify({"erro": "Não autenticado."}), 401

    usuario_id = session["usuario_id"]

    service = EstoqueService(usuario_id=usuario_id)

    if request.method == "POST":
        dados = request.get_json(silent=True) or {}

        try:
            nome = dados.get("nome", "")
            preco = float(dados["preco"])
            quantidade = int(dados["quantidade"])

            service.cadastrar(nome, preco, quantidade)

            return jsonify({
                "mensagem": "Produto cadastrado com sucesso!"
            }), 201

        except (ValueError, TypeError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    produtos = service.listar()

    return jsonify([
        {
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade
        }
        for produto in produtos
    ])

@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def excluir_produto(produto_id):
    if "usuario_id" not in session:
        return jsonify({"erro": "Não autenticado."}), 401

    usuario_id = session["usuario_id"]
    service = EstoqueService(usuario_id=usuario_id)

    try:
        service.remover_por_id(produto_id)
        return jsonify({"mensagem": "Produto excluído com sucesso!"}), 200
    except LookupError as erro:
        return jsonify({"erro": str(erro)}), 404

@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    if "usuario_id" not in session:
        return jsonify({"erro": "Não autenticado."}), 401

    usuario_id = session["usuario_id"]
    service = EstoqueService(usuario_id=usuario_id)

    dados = request.get_json(silent=True) or {}

    try:
        novo_preco = float(dados["preco"])
        nova_quantidade = int(dados["quantidade"])

        service.editar(
            produto_id,
            novo_preco,
            nova_quantidade
        )

        return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

    except (ValueError, TypeError, KeyError) as erro:
        return jsonify({"erro": str(erro)}), 400

    except LookupError as erro:
        return jsonify({"erro": str(erro)}), 404

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("pagina_login"))

if __name__ == "__main__":
    app.run(debug=True)
