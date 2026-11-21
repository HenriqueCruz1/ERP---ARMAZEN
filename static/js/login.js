
const formulario = document.getElementById("form-login");

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const login = document.getElementById("login").value;
    const senha = document.getElementById("senha").value;

    const resposta = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            login: login,
            senha: senha
        })
    });

    const dados = await resposta.json();

    const mensagem = document.getElementById("mensagem");

    if (resposta.ok) {
        window.location.href = "/";
    } else {
        mensagem.textContent = dados.erro;
    }
});
