import qrcode
from pypix import Pix

def gerar_pix_qrcode(chave_pix, nome_recebedor, cidade, valor, descricao):
    # Cria o payload Pix
    pix = Pix(
        chave=chave_pix,
        nome_recebedor=nome_recebedor,
        cidade=cidade,
        valor=valor,
        descricao=descricao
    )

    # Gera o código Pix
    pix_code = pix.payload()

    # Gera o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pix_code)
    qr.make(fit=True)

    # Cria a imagem do QR Code
    img = qr.make_image(fill='black', back_color='white')

    return img