document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Evita o envio tradicional do formulário

    // Captura os dados do formulário
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    data.itens = []; // Adiciona os itens do pedido

    document.querySelectorAll(".product-card").forEach(card => {
        const quantity = parseInt(card.querySelector(".quantity span").innerText);
        if (quantity > 0) {
            data.itens.push({
                nome: card.querySelector(".product-name").innerText,
                quantidade: quantity,
                preco: parseFloat(
                    card.querySelector(".product-price").innerText.replace('R$', '').replace(',', '.')
                )
            });
        }
    });

    // Envia os dados ao backend
    fetch("/imprimir-pedido/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === "success") {
            alert("Pedido enviado para impressão com sucesso!");
        } else {
            alert("Erro ao imprimir: " + result.message);
        }
    })
    .catch(error => console.error("Erro:", error));
});
let subtotal = 0; // Subtotal inicial
let taxaEntrega = 0; // Taxa de entrega inicial

// Função para formatar valores como moeda brasileira
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(value);
}

function addItem(button) {
    const quantitySpan = button.nextElementSibling;
    const quantityValue = quantitySpan.querySelector('span');
    const productCard = button.closest('.product-card');
    const productPrice = parseFloat(
        productCard.querySelector('.product-price').innerText.replace('R$', '').replace(',', '.').trim()
    );

    let currentQuantity = parseInt(quantityValue.innerText);

    // Incrementa a quantidade
    currentQuantity++;
    quantityValue.innerText = currentQuantity;

    // Exibe o contador e o botão de "-" se ainda não estiver visível
    quantitySpan.classList.remove('d-none');

    // Atualiza o subtotal
    subtotal += productPrice;
    updateSubtotal();
    updateTotal();
}

function removeItem(button) {
    const quantitySpan = button.parentElement;
    const quantityValue = quantitySpan.querySelector('span');
    const productCard = button.closest('.product-card');
    const productPrice = parseFloat(
        productCard.querySelector('.product-price').innerText.replace('R$', '').replace(',', '.').trim()
    );

    let currentQuantity = parseInt(quantityValue.innerText);

    // Decrementa a quantidade
    currentQuantity--;
    quantityValue.innerText = currentQuantity;

    // Esconde o contador e o botão de "-" se a quantidade chegar a 0
    if (currentQuantity === 0) {
        quantitySpan.classList.add('d-none');
    }

    // Atualiza o subtotal
    subtotal -= productPrice;
    updateSubtotal();
    updateTotal();
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

    // Adiciona 5% se a forma de pagamento for cartão de crédito
    if (formaPagamento === 'cartaocredito') {
        total = total * 1.05;
    }

    // Atualiza o total na interface
    document.getElementById('total').innerHTML = `<strong>Total: ${formatCurrency(total)}</strong>`;
}
document.getElementById('forma_pagamento').addEventListener('change', updateTotal)

document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Evita o envio tradicional do formulário

    // Captura os dados do formulário
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    data.itens = []; // Adiciona os itens do pedido

    document.querySelectorAll(".product-card").forEach(card => {
        const quantity = parseInt(card.querySelector(".quantity span").innerText);
        if (quantity > 0) {
            data.itens.push({
                nome: card.querySelector(".product-name").innerText,
                quantidade: quantity,
                preco: parseFloat(
                    card.querySelector(".product-price").innerText.replace('R$', '').replace(',', '.')
                )
            });
        }
    });

    // Envia os dados ao backend
    fetch("/imprimir-pedido/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === "success") {
            alert("Pedido enviado para impressão com sucesso!");
        } else {
            alert("Erro ao imprimir: " + result.message);
        }
    })
    .catch(error => console.error("Erro:", error));
});
