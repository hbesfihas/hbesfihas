let subtotal = 0; // Subtotal inicial
let taxaEntrega = 0; // Taxa de entrega inicial

// Função para formatar valores como moeda brasileira
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(value);
}
let produtos = {};

function addItem(button) {
    const productCard = button.closest('.product-card');
    const quantitySpan = productCard.querySelector('.quantity span');
    const hiddenInput = productCard.querySelector('input[type="hidden"]');
    let currentQuantity = parseInt(quantitySpan.innerText);

    // Incrementa a quantidade
    currentQuantity++;
    quantitySpan.innerText = currentQuantity;
    hiddenInput.value = currentQuantity;

    // Exibe o contador se ainda estiver oculto
    productCard.querySelector('.quantity').classList.remove('d-none');
    console.log(`Adicionado: ${productCard.querySelector('.product-name').innerText} - Quantidade: ${currentQuantity}`);
}

function removeItem(button) {
    const productCard = button.closest('.product-card');
    const quantitySpan = productCard.querySelector('.quantity span');
    const hiddenInput = productCard.querySelector('input[type="hidden"]');
    let currentQuantity = parseInt(quantitySpan.innerText);

    // Decrementa a quantidade
    currentQuantity = Math.max(0, currentQuantity - 1); // Evita valores negativos
    quantitySpan.innerText = currentQuantity;
    hiddenInput.value = currentQuantity;

    // Esconde o contador se a quantidade for 0
    if (currentQuantity === 0) {
        productCard.querySelector('.quantity').classList.add('d-none');
    }
    console.log(`Removido: ${productCard.querySelector('.product-name').innerText} - Quantidade: ${currentQuantity}`);
}

function enviarPedido() {
    const produtos = [];

    // Captura os produtos e quantidades
    document.querySelectorAll('.product-card').forEach(card => {
        const nome = card.querySelector('.product-name').innerText.trim(); // Nome do produto
        const quantidade = parseInt(card.querySelector('input[type="hidden"]').value); // Quantidade selecionada

        if (quantidade > 0) {
            produtos.push({ nome, quantidade });
        }
    });

    // Verifica se há pelo menos um produto selecionado
    if (produtos.length === 0) {
        alert("Selecione pelo menos um produto para finalizar o pedido.");
        return;
    }

    console.log("Produtos enviados:", produtos);

    // Preenche os campos ocultos com os valores corretos
    document.getElementById('form-produtos').value = JSON.stringify(produtos);
    document.getElementById('form-endereco').value = document.getElementById('endereco').value.trim();
    document.getElementById('form-subtotal').value = document.getElementById('subtotal-value').value.trim();
    document.getElementById('form-total').value = document.getElementById('total').innerText.replace('R$', '').replace(',', '.').trim();
    document.getElementById('form-taxa-entrega').value = document.getElementById('taxa-entrega').innerText.replace('R$', '').replace(',', '.').trim();
    document.getElementById('form-troco').value = document.getElementById('troco').value.trim();
    document.getElementById('form-bairro').value = document.getElementById('bairro').value.trim();
    document.getElementById('form-pagamento').value = document.getElementById('forma_pagamento').value.trim();

    // Submete o formulário
    document.getElementById('pedido-form').submit();
}


function updateSubtotal() {
    // Atualiza o subtotal na interface
    document.getElementById('subtotal').innerHTML = `<strong>Subtotal: ${formatCurrency(subtotal)}</strong>`;
}

function updateTotal() {
    // Obtém o elemento select de bairros
    const bairroSelect = document.getElementById('bairro');
    const selectedOption = bairroSelect.options[bairroSelect.selectedIndex];

    // Garante que há um bairro selecionado antes de prosseguir
    if (!selectedOption || selectedOption.value === "") {
        taxaEntrega = 0;
    } else {
        // Obtém a taxa de entrega do atributo data-taxa e converte para float
        taxaEntrega = parseFloat(selectedOption.getAttribute('data-taxa').replace(',', '.')) || 0;
    }

    // Atualiza a taxa de entrega na interface
    document.getElementById('taxa-entrega').innerHTML = `<strong>Taxa de Entrega: ${formatCurrency(taxaEntrega)}</strong>`;

    // Verifica a forma de pagamento
    const pagamentoSelect = document.getElementById('forma_pagamento');
    const formaPagamento = pagamentoSelect.value;
    
    // Calcula o total
    let total = subtotal + taxaEntrega;
   
    // Exibição condicional para o campo de Acréscimo
    const acrescimoDiv = document.getElementById('acrescimo');
    let acrescimo = 0;

    if (formaPagamento === 'cartaocredito') {
        acrescimo = total * 0.05;
        acrescimoDiv.innerHTML = `<strong>Taxa cartão de Crédito (5%): ${formatCurrency(acrescimo)}</strong>`;
        acrescimoDiv.classList.remove('d-none');
    } else {
        acrescimoDiv.classList.add('d-none');
    }

     // Exibição condicional para o campo de Troco
     const trocoDiv = document.getElementById('campo-troco');
     if (formaPagamento === 'dinheiro') {
         trocoDiv.classList.remove('d-none');
     } else {
         trocoDiv.classList.add('d-none');
     }
 
     // Calcula o total final
     total += acrescimo;

    // Atualiza o total na interface
    document.getElementById('total').innerHTML = `<strong>Total: ${formatCurrency(total)}</strong>`;

}

