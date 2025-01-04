from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Produto, Bairro, Pedido
from django.contrib.auth import login
from .forms import EntradaForm
import json
from .utils import gerar_pix_qrcode, gerar_pix_copiaecola
from django.views.decorators.csrf import csrf_exempt

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
    if not request.user.is_authenticated:
        return redirect('login')  # Redireciona para a página de login, se o usuário não estiver autenticado
    
    pedidos = Pedido.objects.filter(user=request.user).order_by('-criado_em')  # Filtra os pedidos do usuário autenticado
    return render(request, 'pedidos.html', {'pedidos': pedidos})

def limpar_valor(valor_str):
    """Remove caracteres não numéricos e converte a string para float."""
    try:
        valor_str = valor_str.replace('R$', '').replace(' ', '').replace('\xa0', '').replace(',', '.')
        return float(valor_str)
    except ValueError:
        return 0.0


def gerar_pix_qrcode_view(request):
    chave_pix = "63981216616"
    nome_recebedor = "HB Esfihas"
    cidade = "Pedro Afonso"
    valor = criar_pedido.total  # Valor da transação
    descricao = "Descrição do pagamento"

    # Gera o QR Code
    img = gerar_pix_qrcode(chave_pix, nome_recebedor, cidade, valor, descricao)
    codigo_pix = gerar_pix_copiaecola(chave_pix, nome_recebedor, cidade, valor, descricao)
    # Retorna a imagem como resposta HTTP
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response, JsonResponse({"codigo_pix": codigo_pix})

# @login_required

@csrf_exempt
def criar_pedido(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Recebe os dados enviados do frontend
        
        bairro = Bairro.objects.get(id=data['bairro'])

        try:          
            # Criação do objeto Pedido
            pedido = Pedido.objects.create(
                user=request.user,  # Encontre o usuário pelo username (ou ID, conforme sua necessidade)
                endereco=data['endereco'],
                itens=data['itens'],
                subtotal=data['subtotal'],
                total=data['total'],
                taxa_entrega=data['taxa_entrega'],
                taxa_cartao=data['taxa_cartao'],
                troco=data.get('troco', None),  # O troco pode ser None, caso não seja enviado
                bairro=bairro,
                forma_pagamento=data['forma_pagamento']
            )
            return JsonResponse({
                'status': 'success', 
                'pedido_id': pedido.id, 
                'redirect_url': reverse('pedidos')
                }, status=201) 

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
           
def contato(request):
    return render(request, 'contato.html')

def atualizar_status(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        novo_status = request.POST.get('status')
        if novo_status in dict(Pedido.STATUS_CHOICES).keys():
            pedido.status = novo_status
            pedido.save()
            return JsonResponse ({'status': 'success', 'message': 'Status atualizado com sucesso'})
        else:
            return JsonResponse ({'status': 'error', 'message': 'Status inválido'})
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})