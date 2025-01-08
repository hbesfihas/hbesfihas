let produtos = {}; // Objeto para armazenar produtos e suas quantidades
let subtotal = 0; // Inicializa o subtotal

// Função para formatar valores como moeda brasileira
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(value);
}

function addItem(button, id) {
    
    const quantitySpan = button.previousElementSibling;
    const quantityValue = quantitySpan.querySelector('span');
    const productCard = button.closest('.product-card');
    const productPrice = parseFloat(
        productCard.querySelector('.product-price').textContent.replace('R$', '').replace(',', '.').trim()
    )

    // Localiza o campo <input hidden> correspondente
    const quantidadeInput = productCard.querySelector('input[type="hidden"]');

    let currentQuantity = parseInt(quantityValue.innerText);

    // Incrementa a quantidade
    currentQuantity++;
    quantityValue.innerText = currentQuantity;

    // Atualiza o valor do <input hidden>
    quantidadeInput.value = currentQuantity;

    // Exibe o contador e o botão de "-" se ainda não estiver visível
    
    quantitySpan.classList.remove('d-none');

    // Atualiza o objeto produtos
    if (!produtos[id]) {
        produtos[id] = { quantidade: quantidadeInput, preco: productPrice, nome: productCard.querySelector('.product-name').innerText };
    }
    produtos[id].quantidade = currentQuantity;

    // Atualiza o subtotal
    subtotal += productPrice;
    updateSubtotal();
    updateTotal();
}

function removeItem(button, id) {
    const quantitySpan = button.parentElement;
    const quantityValue = quantitySpan.querySelector('span');
    const productCard = button.closest('.product-card');
    const productPrice = parseFloat(
        productCard.querySelector('.product-price').textContent.replace('R$', '').replace(',', '.').trim()
    )
    // Localiza o campo <input hidden> correspondente
    const quantidadeInput = productCard.querySelector('input[type="hidden"]');

    let currentQuantity = parseInt(quantityValue.innerText);

    // Decrementa a quantidade
    if (currentQuantity > 0) {
        currentQuantity--;
        quantityValue.innerText = currentQuantity;

        // Atualiza o valor do <input hidden>
        quantidadeInput.value = currentQuantity;

        // Esconde o contador e o botão de "-" se a quantidade chegar a 0
        if (currentQuantity === 0) {
            quantitySpan.classList.add('d-none');
            delete produtos[id]; // Remove o produto do objeto se a quantidade for 0
        } else {
            produtos[id].quantidade = currentQuantity; // Atualiza a quantidade no objeto
        }

        if (!produtos[id]) {
            produtos[id] = { quantidade: quantidadeInput, preco: productPrice, nome: productCard.querySelector('.product-name').innerText };
        }
        produtos[id].quantidade = currentQuantity;

        // Atualiza o subtotal
        subtotal -= productPrice;
        updateSubtotal();
        updateTotal();
    }
}

function updateSubtotal() {
    // Atualiza o subtotal na interface
    document.getElementById('subtotal-value').innerText = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    document.getElementById('subtotal-hidden').value = subtotal.toFixed(2).replace('.', ',');
}

function updateTotal() {
    const bairroSelect = document.getElementById('bairro');
    const selectedOption = bairroSelect.options[bairroSelect.selectedIndex];
    const taxaEntregaStr = selectedOption ? selectedOption.getAttribute('data-taxa') : '0';
    const taxaEntrega = parseFloat(taxaEntregaStr) || 0;


    // Atualiza a taxa de entrega no DOM
    document.getElementById('taxa-entrega').querySelector('.value').innerText = `R$ ${taxaEntrega.toFixed(2).replace('.', ',')}`;

    // Calcula o acréscimo (5% para cartão de crédito)
    const formaPagamento = document.getElementById('forma_pagamento').value;
    let acrescimo = 0;
    const acrescimoDiv = document.getElementById('acrescimo-value');
    if (formaPagamento === 'cartaocredito') {
        acrescimo = subtotal * 0.05; // 5% de acréscimo
        acrescimoDiv.classList.remove('d-none');
        acrescimoDiv.querySelector('.value').innerText = acrescimo.toFixed(2).replace('.', ',');
    } else {
        acrescimoDiv.classList.add('d-none');
    }

    // Ex ibição condicional do campo de Troco
    const trocoDiv = document.getElementById('campo-troco');
    if (formaPagamento === 'dinheiro') {
        trocoDiv.classList.remove('d-none');
    } else {
        trocoDiv.classList.add('d-none');
    }
    updateItensPedido();
    // Calcula o total final
    const total = subtotal + taxaEntrega + acrescimo;
    document.getElementById('total-value').innerText = `R$ ${total.toFixed(2).replace('.', ',')}`;
    document.getElementById('form-total').value = total.toFixed(2).replace('.', ',');
}

// Adiciona um listener para mostrar o campo de troco se a forma de pagamento for dinheiro
document.getElementById('forma_pagamento').addEventListener('change', function () {
    const trocoField = document.getElementById('campo-troco');
    if (this.value === 'dinheiro') {
        trocoField.classList.remove('d-none');
    } else {
        trocoField.classList.add('d-none');
    }
});

function updateItensPedido() {
    const itensLista = document.getElementById('itens-lista');
    itensLista.innerHTML = ''; // Limpa a lista de itens

    for (const produtoId in produtos) {
        const produto = produtos[produtoId];
        const li = document.createElement('li');
        li.innerText = `${produto.nome}: ${produto.quantidade}`;
        itensLista.appendChild(li);
    }
}

function enviarPedido() {
    const bairroPedido = document.getElementById("bairro").value; 
    const formaPagamento = document.querySelector("#forma_pagamento").value;
    const enderecoPedido = document.querySelector("#endereco").value;
    const trocoPedido = parseFloat(document.querySelector("#troco")?.value || null);
    const subtotalPedido = parseFloat(document.querySelector("#subtotal-value").textContent.replace("R$", "").replace(",", ".").trim());
    const totalPedido = parseFloat(document.querySelector("#total-value").textContent.replace("R$", "").replace(",", ".").trim());
    const itensPedidoData = document.getElementById("itens-pedido").textContent.trim();
    const itensPedido = itensPedidoData.replace(/^\s+|\s+$/gm, '').replace(/([a-zA-Záéíóúçãêô ]+):/g, '\n$1:').replace(/^\n/, '');;
    const taxaEntregaPedido = parseFloat(document.querySelector("#taxa-entrega .value").textContent.trim().replace("R$", "").replace(",","."));
    const acrescimoPedido = parseFloat(document.querySelector('#acrescimo-value .value').textContent.trim().replace("R$", "").replace(",","."));
    
     
    const pedido = {
        endereco: enderecoPedido,
        itens: itensPedido, 
        subtotal: subtotalPedido,
        total: totalPedido,
        taxa_entrega: taxaEntregaPedido,
        taxa_cartao: acrescimoPedido,
        troco: trocoPedido,
        bairro: bairroPedido,
        forma_pagamento: formaPagamento,
    }
   

    // Verifica se o bairro está preenchido
    if (!bairro.value) {
        alert('Por favor, selecione um bairro.');
        bairro.focus();
        return;
    }

    //  Verifica se o endereço está preenchido
    if (!endereco.value.trim()) {
        alert('Por favor, preencha o campo de endereço.');
        endereco.focus();
        return;
    }

    //  Verifica se a forma de pagamento está preenchida
    if (!formaPagamento) {
        alert('Por favor, selecione uma forma de pagamento.');
        document.getElementById('forma_pagamento').focus();
        return;
    }

    // Verifica o campo de troco, se necessário
    if (formaPagamento.value === 'dinheiro' && (!troco.value || parseFloat(troco.value) <= 0)) {
        alert('Por favor, informe o valor para troco.');
        troco.focus();
        return;
    }
     // Enviar o pedido via fetch
     fetch('/criar_pedido/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // Se CSRF estiver ativo
        },
        body: JSON.stringify(pedido)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(`Pedido realizado com sucesso! ID do pedido: ${data.pedido_id}`);
            window.location.href = data.redirect_url;
        } else {
            alert('Erro ao criar o pedido: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao enviar o pedido.');
    });
    // Submeter o formulário 

}


function alterarStatus(pedidoId, novoStatus) {
    fetch(`/alterar_status/${pedidoId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ status: novoStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Status alterado: ' + novoStatus);
            location.reload();
        } else {
            alert('Erro ao alterar status: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao alterar status.');
    });
}

