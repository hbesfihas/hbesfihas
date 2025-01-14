function selecionarOpcao(opcao) {
    const btnDelivery = document.getElementById('btn-delivery');
    const btnRetirada = document.getElementById('btn-retirada');
    const campoBairro = document.getElementById('campo-bairro');
    const selectBairro = document.getElementById('bairro');
    const enderecoContainer = document.getElementById('endereco-container');
    const enderecoInput = document.getElementById('endereco');
    const campoMapa = document.getElementById('mapa-retirada');

    if (opcao === 'delivery') {
        // Configuração para Delivery
        btnDelivery.classList.add('active', 'btn-primary');
        btnDelivery.classList.remove('btn-secondary');
        btnRetirada.classList.add('btn-secondary');
        btnRetirada.classList.remove('active', 'btn-primary');
        campoMapa.classList.add('d-none');


        // Reativa o campo de bairro e limpa a seleção
        selectBairro.disabled = false;
        selectBairro.value = ""; // Reseta o campo para "Selecione um bairro"
        enderecoContainer.style.display = 'block'; // Mostra o campo de endereço
        campoBairro.classList.remove('d-none');
        selectBairro.display = 'block';

    } 
     if (opcao === 'retirada') {
        // Configuração para Retirada
        btnRetirada.classList.add('active', 'btn-primary');
        btnRetirada.classList.remove('btn-secondary');
        btnDelivery.classList.add('btn-secondary');
        btnDelivery.classList.remove('active', 'btn-primary');
        campoBairro.classList.add('d-none');
        campoMapa.classList.remove('d-none');

        // Seleciona automaticamente o bairro "Retirada"
        const optionRetirada = [...selectBairro.options].find(opt => opt.text.includes('Retirada'));
        if (optionRetirada) {
            selectBairro.value = optionRetirada.value;
        }
        selectBairro.disabled = true; // Desativa o campo de bairro

        // Preenche automaticamente o campo de endereço para passar na validação
        enderecoInput.value = "Retirada no local"; // Valor fictício que passa na validação
        enderecoContainer.style.display = 'none'; // Oculta o campo de endereço
        
    }
}

// Define o estado inicial como Delivery
document.addEventListener('DOMContentLoaded', () => selecionarOpcao('delivery'));



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
    );
    const quantidadeInput = productCard.querySelector('input[type="hidden"]');
    const productName = productCard.querySelector('.product-name').innerText; // Nome do produto para manipular a lista

    let currentQuantity = parseInt(quantityValue.innerText);

    // Decrementa a quantidade
    if (currentQuantity > 0) {
        currentQuantity--;
        quantityValue.innerText = currentQuantity;

        // Atualiza o valor do <input hidden>
        quantidadeInput.value = currentQuantity;

        // Se a quantidade chegar a 0, esconde o contador e remove o item da lista
        if (currentQuantity === 0) {
            quantitySpan.classList.add('d-none');

            // Remove o produto do objeto
            delete produtos[id];

            // Remove o item correspondente da lista pelo nome do produto
            const itensLista = document.querySelector('#itens-lista');
            const listaItens = itensLista.querySelectorAll('li');
            listaItens.forEach((item) => {
                if (item.textContent.startsWith(`${productName}:`)) {
                    item.remove(); // Remove o item da lista
                }
            });
        } else {
            produtos[id].quantidade = currentQuantity; // Atualiza a quantidade no objeto

            // Atualiza o item da lista com a nova quantidade
            const itensLista = document.querySelector('#itens-lista');
            const listaItens = itensLista.querySelectorAll('li');
            listaItens.forEach((item) => {
                if (item.textContent.startsWith(`${productName}:`)) {
                    item.textContent = `${productName}: ${currentQuantity}`; // Atualiza o texto
                }
            });
        }

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
    document.getElementById('subtotal-fixed-value').innerText = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
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
    const imagemCartao = document.getElementById('imagem-maquininha');
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
    if (formaPagamento === 'cartaodebito'|| formaPagamento === 'cartaocredito'){
        imagemCartao.classList.remove('d-none');
    } else {
        imagemCartao.classList.add('d-none');
    }
    updateItensPedido();
    // Calcula o total final
    const total = subtotal + taxaEntrega + acrescimo;
    document.getElementById('total-value').innerText = `R$ ${total.toFixed(2).replace('.', ',')}`;
    document.getElementById('form-total').value = total.toFixed(2).replace('.', ',');
}


document.getElementById('forma_pagamento').addEventListener('change', function(){
    const pixField = document.getElementById('campo-pix');
    if (this.value === 'pix') {
        pixField.classList.remove('d-none');
    } else {
        pixField.classList.add('d-none');
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
        return false;
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
            alert(`Pedido realizado com sucesso! ID do pedido: ${data.pedido_id}\n Acompanhe seu pedido em Meus Pedidos`);
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

document.addEventListener('DOMContentLoaded', function () {

    const summaryContainer = document.querySelector('.summary-container');
    const fixedSubtotal = document.querySelector('#subtotal-fixed');
    
    function updateFixedSubtotal() {
        const summaryTop = summaryContainer.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
    
        if (summaryTop <= windowHeight) {
            fixedSubtotal.classList.add('d-none'); // Oculta o subtotal fixo
        } else {
            fixedSubtotal.classList.remove('d-none'); // Mostra o subtotal fixo
        }
    }

    // Atualiza o subtotal fixo ao rolar ou quando houver mudanças no subtotal original
    window.addEventListener('scroll', updateFixedSubtotal);

    // Sincroniza inicialmente ao carregar a página
    updateFixedSubtotal();
});

// AREA DO PIX

// Dados fixos do recebedor
const name = "Breno";
const pixKey = "+5563981216616";
const city = "Pedro Afonso";
const textIdentifier = "HBESFIHAS";

// Função para gerar o payload Pix
function generatePixPayload(name, pixKey, city, textIdentifier, totalValue) {
    const totalFormatted = totalValue.padStart(2, "0").trim(); // Exemplo: 23.90 
    const merchantAccountInfo = `0014BR.GOV.BCB.PIX01${pixKey.length.toString().padStart(2, '0')}${pixKey}`;
    const additionalDataField = `05${textIdentifier.length.toString().padStart(2, '0')}${textIdentifier}`;

    const payload = [
        '000201', // Payload Format Indicator
        `26${merchantAccountInfo.length.toString().padStart(2, '0')}${merchantAccountInfo}`, // Merchant Account Info
        '52040000', // Merchant Category Code
        '5303986', // Transaction Currency (BRL)
        `54${totalFormatted.length.toString().padStart(2, '0')}${totalFormatted}`, // Transaction Amount
        '5802BR', // Country Code
        `59${name.length.toString().padStart(2, '0')}${name}`, // Merchant Name
        `60${city.length.toString().padStart(2, '0')}${city}`, // Merchant City
        `62${additionalDataField.length.toString().padStart(2, '0')}${additionalDataField}`, // Additional Data Field
        '6304' // CRC Placeholder
    ].join('');

    // Calcula o CRC16
    const crc16 = crc16Calculator(payload);
    return `${payload}${crc16}`;
}

// Função para calcular o CRC16
function crc16Calculator(payload) {
    const polynomial = 0x1021;
    let crc = 0xFFFF;

    for (let i = 0; i < payload.length; i++) {
        const byte = payload.charCodeAt(i);
        crc ^= (byte << 8);

        for (let j = 0; j < 8; j++) {
            if ((crc & 0x8000) !== 0) {
                crc = (crc << 1) ^ polynomial;
            } else {
                crc <<= 1;
            }
        }

        crc &= 0xFFFF;
    }

    return crc.toString(16).toUpperCase().padStart(4, '0');
}

// Função para atualizar o campo Pix quando necessário
function updatePixField() {
    const formaPagamento = document.getElementById('forma_pagamento').value;
    const pixField = document.getElementById('campo-pix');
    const totalValue = document.getElementById('form-total').value.replace(',','.');

    if (formaPagamento === 'pix') {
        const pixPayload = generatePixPayload(name, pixKey, city, textIdentifier, totalValue);
        document.getElementById('pix-copia-e-cola').value = pixPayload;
        pixField.classList.remove('d-none');
    } else {
        pixField.classList.add('d-none');
    }
}

// Adiciona o evento no dropdown de forma de pagamento
document.getElementById('forma_pagamento').addEventListener('change', updatePixField);

// Função para copiar o Pix para a área de transferência
function copiarPix() {
    const pixText = document.getElementById('pix-copia-e-cola');
    pixText.select(); // Seleciona o texto no campo
    pixText.setSelectionRange(0, 99999); // Para dispositivos móveis

    try {
        document.execCommand('copy');
        alert('Chave Pix copiada para a área de transferência!\n Seu pedido será enviado');
        document.getElementById('btn-enviar-pedido').click();
    } catch (err) {
        alert('Erro ao copiar a chave Pix.');
    }
}

// Adiciona o evento ao botão de copiar Pix
document.getElementById('botao-copiar-pix').addEventListener('click', function (event) {
    event.preventDefault(); // Impede o botão de submeter o formulário
    copiarPix();

    
});

function imprimirPedido(pedidoId) {
    // Localiza o card do pedido específico pelo ID
    const pedidoCard = document.querySelector(`[onclick="imprimirPedido(${pedidoId})"]`).closest('.card');

    if (pedidoCard) {
        // Extrai os dados do pedido para impressão
        const pedidoIdText = pedidoCard.querySelector('.card-header div').innerText.replace('ID do ',''); // ID do pedido
        const clienteText = pedidoCard.querySelector('div:nth-child(3)').innerText; // Cliente
        const itensText = pedidoCard.querySelector('textarea').value.trim(); // Itens do pedido (em forma de lista)

        // Lógica para contar a quantidade total de produtos
        let totalProdutos = 0;

        if (itensText) {
            const linhas = itensText.split('\n'); // Divide o texto em linhas
            let isItensSection = false; // Flag para saber quando estamos na seção de itens do pedido
            linhas.forEach((linha) => {
                linha = linha.trim(); // Remove espaços no início e no final

                // Ignora a primeira linha do cabeçalho ("Itens do Pedido: Quantidade")
                if (linha.includes("Itens do Pedido: Quantidade") || linha === "") {
                    return;
                }

                // Se a linha contiver ":", provavelmente é um item do pedido com quantidade
                if (linha.includes(':')) {
                    const partes = linha.split(':'); // Divide pelo ":"
                    if (partes.length > 1) {
                        const quantidade = parseInt(partes[1].trim(), 10); // Extrai a quantidade após ":"
                        if (!isNaN(quantidade)) {
                            totalProdutos += quantidade; // Soma a quantidade ao total
                        }
                    }
                }
            });
        }

        // Cria o layout HTML para a impressão
        const htmlImpressao = `
            <html>
                <head>
                    <title>Impressão de Pedido</title>
                    <style>
                        body {
                            font-family: calibri;
                            font-size: 20px;
                            margin: 0;
                            padding: 10px;
                            width: 55mm; /* Ideal para impressoras térmicas */
                        }
                        h1, h2, h3 {
                            text-align: center;
                            margin: 5px 0;
                        }
                        .pedido-info {
                            margin-bottom: 10px;
                        }
                        .pedido-info div {
                            margin: 5px 0;
                        }
                        .itens {
                            margin-top: 10px;
                            text-align: right;
                        }
                        .itens div {
                            margin: 2px 0;
                        }
                        hr {
                            border: none;
                            border-top: 1px dashed #000;
                            margin: 5px 0;
                        }
                        .footer {
                            text-align: center;
                            margin-top: 10px;
                            font-size: 12px;
                        }
                    </style>
                </head>
                <body>
                    <h2>${pedidoIdText}</h2>
                    <div>${clienteText}</div>
                    <hr>
                    <div class="itens">${itensText.replace(/\n/g, '<br>')}</div>
                    <hr>
                    <div class="itens"><strong>Total de Produtos:</strong> ${totalProdutos}</div>
                </body>
            </html>
        `;

        // Envia para a impressão
        const janelaImpressao = window.open('', '_blank', 'width=600,height=800');
        janelaImpressao.document.write(htmlImpressao);

        // Fecha a janela de impressão após carregar
        janelaImpressao.document.close();
        janelaImpressao.print();
    } else {
        alert('Pedido não encontrado!');
    }
}

const eventoSSE = new EventSource('/sse-pedidos/');

eventoSSE.onmessage = function (event){
    const novosPedidos = JSON.parse(event.data);

    if (novosPedidos){
        const audio = new Audio('/static/audio/notification.mp3');
        audio.play();

        alert('Novo pedido recebido!');
    }
};


function imprimirPedidoCompleto(pedidoId){
    const pedidoCard = document.querySelector(`[onclick="imprimirPedido(${pedidoId})"]`).closest('.card');

    if (pedidoCard) {
        const pedidoIdText = pedidoCard.querySelector('.card-header div').innerText.replace('ID do ',''); // ID do pedido
        const pagoText = pedidoCard.querySelector('div:nth-last-child(9)').innerText;
        const dataText = pedidoCard.querySelector('div:nth-last-child(8)').innerText;
        const clienteText = pedidoCard.querySelector('div:nth-child(3)').innerText; // Cliente
        const enderecoText = pedidoCard.querySelector('div:nth-child(4)').innerText;
        const itensText = pedidoCard.querySelector('textarea').value.trim(); // Itens do pedido (em forma de lista)
        const subtotalText = pedidoCard.querySelector('div:nth-child(7)').innerText;
        const totalText = pedidoCard.querySelector('div:nth-child(8) input')?.value || 'Total não disponível';
        const formaPagamentoText = pedidoCard.querySelector('div:nth-child(9)').innerText;
        const bairroText = pedidoCard.querySelector('div:nth-last-child(5)').innerText;
        var trocoText = "=)";
        if (formaPagamentoText == "Forma de Pagamento: dinheiro"){
        trocoText = pedidoCard.querySelector('div:nth-child(10)').innerText;}
    


           // Lógica para contar a quantidade total de produtos
           let totalProdutos = 0;

           if (itensText) {
               const linhas = itensText.split('\n'); // Divide o texto em linhas
               let isItensSection = false; // Flag para saber quando estamos na seção de itens do pedido
               linhas.forEach((linha) => {
                   linha = linha.trim(); // Remove espaços no início e no final
       
                   // Ignora a primeira linha do cabeçalho ("Itens do Pedido: Quantidade")
                   if (linha.includes("Itens do Pedido: Quantidade") || linha === "") {
                       return;
                   }
       
                   // Se a linha contiver ":", provavelmente é um item do pedido com quantidade
                   if (linha.includes(':')) {
                       const partes = linha.split(':'); // Divide pelo ":"
                       if (partes.length > 1) {
                           const quantidade = parseInt(partes[1].trim(), 10); // Extrai a quantidade após ":"
                           if (!isNaN(quantidade)) {
                               totalProdutos += quantidade; // Soma a quantidade ao total
                           }
                       }
                   }
               });
           }
               // Cria o layout HTML para a impressão
               const htmlImpressao = `
                   <html>
                       <head>
                           <title>Impressão de Pedido</title>
                           <style>
                               body {
                                   font-family: calibri;
                                   font-size: 14px;
                                   margin: 0;
                           
                                   width: 50mm; /* Ideal para impressoras térmicas */
                               }
                               h1, h2, h3 {
                                   text-align: center;
                                   margin: 5px 0;
                               }
                               .pedido-info {
                                   margin-bottom: 10px;
                               }
                               .pedido-info div {
                                   margin: 5px 0;
                                   text-align: right;
                               }
                               .itens {
                                   margin-top: 10px;
                                   text-align: right;
                               }
                               .itens div {
                                   margin: 2px 0;
                               }
                               hr {
                                   border: none;
                                   border-top: 1px dashed #000;
                                   margin: 5px 0;
                               }
                               .footer {
                                   text-align: center;
                                   margin-top: 10px;
                                   font-size: 12px;
                               }
                           </style>
                       </head>
                       <body>
                           <h1>HB Esfihas</h1>
                           <h2>${pedidoIdText}</h2>
                           <h3>${clienteText}</h3>
                           <hr>
                           <div class="pedido-info">
                               <div>${pagoText}</div>
                               <div>${dataText}</div>
                             
                               <div> ${enderecoText}</div>
                               <div> ${bairroText} </div>
                           </div>
                           <hr>
                           <div class="itens">${itensText.replace(/\n/g, '<br>')}</div>
                           <hr>
                           <div class="pedido-info">
                              <div><strong>Qnt. Total de itens:</strong> ${totalProdutos}</div>
                              <div> ${subtotalText} </div>    
                              <div><strong>Total:</strong> ${totalText}</div>
                              <div>${formaPagamentoText}</div>
                              <div>${trocoText||0}</div>
                           </div>
                           <hr>
                           <div class="footer">
                               Impressão gerada pelo sistema HB Esfihas<br>
                               Obrigado pela preferência!
                           </div>
                       </body>
                   </html>
               `;
       
               // Envia para a impressão
               const janelaImpressao = window.open('', '_blank', 'width=540,height=800');
               janelaImpressao.document.write(htmlImpressao);
       
               // Fecha a janela de impressão após carregar
               janelaImpressao.document.close();
               janelaImpressao.print();
           } else {
               alert('Pedido não encontrado!');
           }
       }
