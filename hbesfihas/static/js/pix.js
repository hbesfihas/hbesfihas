// Dados fixos do recebedor
const name = "Breno";
const pixKey = "+5563981216616";
const city = "Pedro Afonso";
const textIdentifier = "HBESFIHAS";

// Valor total capturado do total do pedido no html home.html
let totalValue = document.getElementById('total-value').textContent.replace("R$", "").replace(",", ".");



// Função para gerar o payload Pix
function generatePixPayload(name, pixKey, city, textIdentifier, totalValue) {
    const totalFormatted = totalValue.padStart(2, "0").trim(); // Exemplo: 23.90 -> "2390"
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

// Gera o payload Pix
 const pixPayload = generatePixPayload(name, pixKey, city, textIdentifier, totalValue);

// Exibe o código Pix no campo de texto
 document.getElementById('pix-copia-e-cola').value = pixPayload;
