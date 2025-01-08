from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import User, Produto, Bairro, Pedido
from django.contrib.auth import login
from .forms import EntradaForm
from django.utils.timezone import localdate
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.paginator import Paginator
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
    
    pedidos_list = Pedido.objects.filter(user=request.user).order_by('-criado_em')  # Filtra os pedidos do usuário autenticado
    
    paginator = Paginator(pedidos_list, 5)
    page_number = request.GET.get('page')
    pedidos = paginator.get_page(page_number)
    
    return render(request, 'pedidos.html', {'pedidos': pedidos})

def limpar_valor(valor_str):
    """Remove caracteres não numéricos e converte a string para float."""
    try:
        valor_str = valor_str.replace('R$', '').replace(' ', '').replace('\xa0', '').replace(',', '.')
        return float(valor_str)
    except ValueError:
        return 0.0


@login_required
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

def gerar_pix(request):
    pass

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def gerencia(request):
    if request.method == 'POST':
        # Atualizar o status do pedido
        pedido_id = request.POST.get('pedido_id')
        novo_status = request.POST.get('status')
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.status = novo_status
        pedido.save()
        
        return JsonResponse({'status': 'success', 'message': 'Status atualizado com sucesso!'})
    pedidos = Pedido.objects.all().order_by('-id')
    return render(request, 'gerencia.html', {'pedidos': pedidos})

def alterar_status(request, pedido_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            novo_status = data.get('status')
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.status = novo_status
            pedido.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "pedidos",
                {
                    'type':'pedido_status_update',
                    'status': novo_status,
                    'pedido_id': pedido_id,
                }
            )
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

@login_required
def atualizar_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by('-id')  # Ordena pelos mais recentes
    return render(request, 'pedidos_lista_parcial.html', {'pedidos': pedidos})

def filtrar_pedidos(request):
    
    return render(request, 'gerencia.html')