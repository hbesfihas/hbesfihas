function prepararParaImpressao() {
    const pedido = [];

    // Recolher os itens do pedido
    const produtos = document.querySelectorAll('.product-card');
    produtos.forEach((produto) => {
        const quantidade = parseInt(produto.querySelector('.quantity span').innerText);
        if (quantidade > 0) {
            const nome = produto.querySelector('.product-name').innerText;
            const preco = produto.querySelector('.product-price').innerText;
            pedido.push({
                nome: nome,
                quantidade: quantidade,
                preco: preco,
            });
        }
    });

    // Recolher os outros detalhes
    const bairroSelect = document.getElementById('bairro');
    const bairroNome = bairroSelect.options[bairroSelect.selectedIndex]?.innerText || '';
    const taxaEntrega = document.getElementById('taxa-entrega').innerText.replace('Taxa de Entrega: ', '');

    const formaPagamentoSelect = document.getElementById('forma_pagamento');
    const formaPagamento = formaPagamentoSelect.options[formaPagamentoSelect.selectedIndex]?.innerText || '';

    const endereco = document.getElementById('endereco').value;
    const total = document.getElementById('total').innerText.replace('Total: ', '');

    // Organizar os dados
    const dadosPedido = {
        itens: pedido,
        bairro: bairroNome,
        taxaEntrega: taxaEntrega,
        formaPagamento: formaPagamento,
        endereco: endereco,
        total: total,
    };

    console.log("Dados do pedido:", dadosPedido); // Para ver o resultado no console

    return dadosPedido;
}

function gerarTextoImpressao(dadosPedido) {
    let textoImpressao = "===== HB Esfihas =====\n";
    textoImpressao += "Pedido:\n";
    dadosPedido.itens.forEach((item) => {
        textoImpressao += `${item.quantidade}x ${item.nome} - ${item.preco}\n`;
    });

    textoImpressao += `\nSubtotal: ${document.getElementById('subtotal').innerText.replace('Subtotal: ', '')}`;
    textoImpressao += `\nTaxa de Entrega: ${dadosPedido.taxaEntrega}`;
    textoImpressao += `\nTotal: ${dadosPedido.total}\n`;

    textoImpressao += "\n=== Detalhes da Entrega ===\n";
    textoImpressao += `Bairro: ${dadosPedido.bairro}\n`;
    textoImpressao += `Endereço: ${dadosPedido.endereco}\n`;
    textoImpressao += `Pagamento: ${dadosPedido.formaPagamento}\n`;

    textoImpressao += "\n==========================\n";
    textoImpressao += "Obrigado por escolher HB Esfihas!";
    
    return textoImpressao;
}

function enviarParaImpressao() {
    const dadosPedido = prepararParaImpressao();
    const textoImpressao = gerarTextoImpressao(dadosPedido);

    // Enviar para o backend via POST
    fetch('/imprimir-pedido/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ texto: textoImpressao }),
    })
    .then((response) => {
        if (response.ok) {
            alert('Pedido enviado para impressão!');
        } else {
            alert('Erro ao enviar pedido para impressão.');
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
        alert('Erro ao enviar pedido para impressão.');
    });
}
