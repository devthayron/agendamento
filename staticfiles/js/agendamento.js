function adicionarProduto() {
    const produtosDiv = document.getElementById('produtos');
    const novoProduto = document.createElement('div');
    novoProduto.classList.add('produto', 'mb-4', 'p-3', 'border', 'rounded', 'bg-white', 'shadow-sm');

    novoProduto.innerHTML = `
        <div class="row g-3">
            <div class="col-md-5">
                <label class="form-label">Nome do Produto</label>
                <input type="text" name="produtos[${index}][nome]" class="form-control" required>
            </div>
            <div class="col-md-3">
                <label class="form-label">Quantidade</label>
                <input type="number" name="produtos[${index}][quantidade]" class="form-control" step="any" required>
            </div>
            <div class="col-md-4">
                <label class="form-label">Cubagem</label>
                <input type="number" name="produtos[${index}][cubagem]" class="form-control" step="any" required>
            </div>
        </div>

        <div class="row mt-3">
            <div class="col-6 d-flex justify-content-end">
                <button type="button" class="btn btn-success w-100" onclick="adicionarProduto()">+ Adicionar</button>
            </div>
            <div class="col-6 d-flex justify-content-start">
                <button type="button" class="btn btn-danger w-100" onclick="removerProduto(this)">Remover</button>
            </div>
        </div>
    `;

    produtosDiv.appendChild(novoProduto);
    index++;
}

function removerProduto(botao) {
    const produto = botao.closest('.produto');
    if (document.querySelectorAll('.produto').length > 1) {
        produto.remove();
    } else {
        alert('Não é possível remover o último produto.');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const mensagemErro = document.querySelector('.alert');

    if (mensagemErro && form) {
        form.addEventListener('submit', function (e) {
            const erroTexto = mensagemErro.textContent || mensagemErro.innerText;
            if (erroTexto.includes('limite de agendamentos')) {
                e.preventDefault();
                alert('Não é possível enviar o formulário: limite de agendamentos atingido.');
            }
        });
    }

    document.querySelectorAll('.usar-data').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const dataSelecionada = this.getAttribute('data-data');
            const inputData = document.querySelector('#id_data_hora');

            if (inputData) {
                const partes = dataSelecionada.split('/');
                const dataFormatada = `${partes[2]}-${partes[1]}-${partes[0]}`;
                inputData.value = dataFormatada;
            }

            mensagemErro.remove();
        });
    });
});
