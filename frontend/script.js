const apiUrl = "http://127.0.0.1:5000/contacts";

function carregarContatos() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById("lista");
            lista.innerHTML = "";

            data.forEach(contato => {
                const li = document.createElement("li");
                li.innerHTML = `
                    ${contato.nome} - ${contato.email}
                    <button onclick="removerContato(${contato.id})">Excluir</button>
                `;
                lista.appendChild(li);
            });
        });
}

function adicionarContato() {
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;

    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ nome, email })
    })
    .then(() => {
        document.getElementById("nome").value = "";
        document.getElementById("email").value = "";
        carregarContatos();
    });
}

function removerContato(id) {
    fetch(`${apiUrl}/${id}`, {
        method: "DELETE"
    })
    .then(() => carregarContatos());
}

carregarContatos();

function enviarCampanha() {
    fetch("http://127.0.0.1:5000/send-campaign", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("resultado").innerText =
            `Campanha enviada para ${data.total} emails.`;
    });
}

function carregarRelatorio() {
    fetch("http://127.0.0.1:5000/reports")
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById("relatorio");
            lista.innerHTML = "";

            data.forEach(item => {
                const li = document.createElement("li");
                li.innerText = `${item.email} - ${item.data}`;
                lista.appendChild(li);
            });
        });
}

function exportarCSV() {
    fetch("http://127.0.0.1:5000/reports/csv")
        .then(() => {
            alert("Relatório CSV gerado no backend!");
        });
}
