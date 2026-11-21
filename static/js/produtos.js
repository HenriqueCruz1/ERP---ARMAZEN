
async function carregarProdutos() {
    const resposta = await fetch("/produtos");

    if (!resposta.ok) {
        console.error("Erro ao carregar produtos.");
        return;
    }

    const produtos = await resposta.json();

    const tabela = document.getElementById("lista-produtos");

    tabela.innerHTML = "";

    produtos.forEach((produto) => {
        const linha = document.createElement("tr");

        linha.innerHTML = `
            <td>${produto.nome}</td>
            <td>R$ ${Number(produto.preco).toFixed(2)}</td>
            <td>${produto.quantidade}</td>
            <td>
                <button class="btn-excluir" data-id="${produto.id}">
                    Excluir
                </button>
            </td>
        `;

        tabela.appendChild(linha);
    });
}

document.addEventListener("DOMContentLoaded", carregarProdutos);

const btnCadastrar = document.getElementById("btn-cadastrar");
const formularioCadastro = document.getElementById("formulario-cadastro");
const btnCancelar = document.getElementById("btn-cancelar");

// Abrir formulário
btnCadastrar.addEventListener("click", () => {
    formularioCadastro.hidden = false;
});

// Fechar formulário
btnCancelar.addEventListener("click", () => {
    formularioCadastro.hidden = true;
});

const formCadastro = document.getElementById("form-cadastro");

formCadastro.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const nome = document.getElementById("nome-produto").value;
    const preco = document.getElementById("preco-produto").value;
    const quantidade = document.getElementById("quantidade-produto").value;

    const resposta = await fetch("/produtos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            preco: preco,
            quantidade: quantidade
        })
    });

    const dados = await resposta.json();

    const mensagem = document.getElementById("mensagem-cadastro");

    if (resposta.ok) {
        mensagem.textContent = dados.mensagem;

        formCadastro.reset();

        await carregarProdutos();

    } else {
        mensagem.textContent = dados.erro;
    }
});

const tabelaProdutos = document.getElementById("lista-produtos");

tabelaProdutos.addEventListener("click", async (evento) => {
    const botao = evento.target.closest(".btn-excluir");

    if (!botao) {
        return;
    }

    const produtoId = botao.dataset.id;

    const confirmar = confirm("Deseja realmente excluir este produto?");

    if (!confirmar) {
        return;
    }

    const resposta = await fetch(`/produtos/${produtoId}`, {
    method: "DELETE"
});

    const dados = await resposta.json();
    
    if (!resposta.ok) {
        alert(dados.erro);
        return;
    }
    
    alert(dados.mensagem);
    await carregarProdutos();
});

const btnAtualizar = document.getElementById("btn-atualizar");

btnAtualizar.addEventListener("click", () => {
    const produtoId = prompt("Digite o ID do produto que deseja atualizar:");

    if (!produtoId) {
        return;
    }

    const novoPreco = prompt("Digite o novo preço:");
    const novaQuantidade = prompt("Digite a nova quantidade:");

    if (novoPreco === null || novaQuantidade === null) {
        return;
    }

    // Vamos conectar à API na próxima etapa.

    fetch(`/produtos/${produtoId}`, {
    method: "PUT",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        preco: novoPreco,
        quantidade: novaQuantidade
    })
})
    .then(async (resposta) => {
        const dados = await resposta.json();

    if (!resposta.ok) {
        alert(dados.erro);
        return;
    }

    alert(dados.mensagem);
    carregarProdutos();

    })

    .catch((erro) => {
        console.error("Erro ao atualizar produto:", erro);
    });

});

const btnLogout = document.getElementById("btn-logout");

btnLogout.addEventListener("click", async () => {
    const resposta = await fetch("/logout", {
        method: "POST"
    });

    if (resposta.redirected) {
        window.location.href = resposta.url;
    }
});