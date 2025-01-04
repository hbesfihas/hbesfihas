from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import ItemPedido, User, Produto, Bairro, Pedido
from django.contrib.auth import login
from .forms import EntradaForm
import json
from .utils import gerar_pix_qrcode, gerar_pix_copiaecola

def home(request):
    user = request.user
    if request.user.is_authenticated:
        produtos = Produto.objects.all()
        bairros = Bairro.objects.all()
        ultimo_pedido = Pedido.objects.filter(user=user).order_by('-criado_em').first()
        if ultimo_pedido:
            endereco = ultimo_pedido.endereco
        else:
            endereco = None
        return render(request, 'home.html', {'produtos': produtos, 'bairros': bairros, 'user': user, 'endereco': endereco})
    else:
        return redirect('login')

def entrada_view(request):
    if request.method == 'POST':
            nome = request.POST.get('nome')
            whatsapp = request.POST.get('whatsapp')


            if not nome or not whatsapp:
                return render(request, 'login.html', {"error": "Nome e Whatsapp são obrigatórios"})
            # Verifica se o usuário já existe ou cria um novo
            user, created = User.objects.get_or_create(
                whatsapp=whatsapp,
                defaults={'nome': nome}
            )

            # Atualiza o nome se o usuário já existir e estiver diferente
            if not created and user.nome != nome:
                user.nome = nome
                user.save()

            # Autentica o usuário
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial
    else:
        form = EntradaForm()

    return render(request, 'login.html', {'form': form})

def pedidos(request):
    return render(request, 'pedidos.html', {'pedidos': pedidos})

@login_required
def finalizar_pedido(request):
    if request.method == "POST":
        try:
            # Dados principais
            user = request.user
            endereco = request.POST.get("endereco")
            subtotal = float(request.POST.get("subtotal", 0))
            total = float(request.POST.get("total", 0))
            taxa_entrega = float(request.POST.get("taxa_entrega", 0))
            taxa_cartao_credito = float(request.POST.get("taxa_cartao_credito", 0))
            troco = float(request.POST.get("troco", 0))
            bairro_id = int(request.POST.get("bairro"))
            forma_pagamento = request.POST.get("forma_pagamento")
            produtos_json = request.POST.get("produtos")

            # Validação
            bairro = get_object_or_404(Bairro, id=bairro_id)
            if not produtos_json:
                return JsonResponse({"message": "Nenhum produto selecionado."}, status=400)

            # Parse dos produtos
            produtos = json.loads(produtos_json)

            # Cria o pedido
            pedido = Pedido.objects.create(
                user=request.user,
                endereco=endereco,
                subtotal=subtotal,
                total=total,
                taxa_entrega=taxa_entrega,
                taxa_cartao_credito=taxa_cartao_credito,
                troco=troco,
                bairro=bairro,
                forma_pagamento=forma_pagamento,
            )

            # Cria os itens do pedido
            for produto in produtos:
                nome = produto["nome"]
                quantidade = produto["quantidade"]
                ItemPedido.objects.create(pedido=pedido, nome=nome, quantidade=quantidade)

            return JsonResponse({"message": "Pedido realizado com sucesso!", "pedido_id": pedido.id}, status=200)

        except Exception as e:
            return JsonResponse({"message": "Erro ao processar o pedido.", "error": str(e)}, status=500)
    return JsonResponse({"message": "Método não permitido."}, status=405)


def gerar_pix_qrcode_view(request):
    chave_pix = "63981216616"
    nome_recebedor = "HB Esfihas"
    cidade = "Pedro Afonso"
    valor = finalizar_pedido.total  # Valor da transação
    descricao = "Descrição do pagamento"

    # Gera o QR Code
    img = gerar_pix_qrcode(chave_pix, nome_recebedor, cidade, valor, descricao)
    codigo_pix = gerar_pix_copiaecola(chave_pix, nome_recebedor, cidade, valor, descricao)
    # Retorna a imagem como resposta HTTP
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response, JsonResponse({"codigo_pix": codigo_pix})