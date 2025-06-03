from decimal import Decimal, InvalidOperation
import time
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import User, Produto, Bairro, Pedido, Categoria, ConfiguracaoLoja
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
        configuracao = get_object_or_404(ConfiguracaoLoja, pk=1)

        if not configuracao.loja_aberta:
            contexto = {
                'mensagem_fechada': configuracao.mensagem_fechada,
                'imagem_fechada': configuracao.imagem_fechada,
            }
            return render(request, 'loja_fechada.html', contexto)

        produtos = Produto.objects.all()
        bairros = Bairro.objects.all()
        categorias = Categoria.objects.all()
        ultimo_endereco = request.user.ultimo_endereco if request.user.ultimo_endereco else ""

        return render(request, 'home.html', {'produtos': produtos, 'bairros': bairros, 'user': user, 'ultimo_endereco': ultimo_endereco, 'categorias':categorias, 'configuracao':configuracao})
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
    configuracao = get_object_or_404(ConfiguracaoLoja, pk=1)
    paginator = Paginator(pedidos_list, 5)
    page_number = request.GET.get('page')
    pedidos = paginator.get_page(page_number)

    return render(request, 'pedidos.html', {'pedidos': pedidos, 'configuracao': configuracao})

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
        try:
            data = json.loads(request.body)  # Recebe os dados enviados do frontend
            endereco = data.get('endereco')

            request.user.ultimo_endereco = endereco
            request.user.save()

            # Validar campos obrigatórios
            if not all(key in data for key in ['bairro', 'forma_pagamento', 'subtotal', 'total', 'itens', 'endereco']):
                raise ValueError("Dados incompletos enviados no pedido.")


            # Converter valores financeiros para Decimal
            try:
                subtotal = Decimal(data['subtotal'])
                total = Decimal(data['total'])
                pontos_necessarios = int(data['pontos_necessarios'])
            except InvalidOperation:
                raise ValueError("Valores financeiros inválidos.")

            bairro = Bairro.objects.get(id=data['bairro'])
            forma_pagamento = data['forma_pagamento']

            # Inicializar os pontos ganhos como 0
            pontos_ganhos = Decimal('0')

            if forma_pagamento == 'pontos':
                pontos_necessarios += int(data['taxa_entrega'])  # Adicionar o valor do frete em pontos

            if forma_pagamento == 'pontos':
                # Verificar se o cliente tem pontos suficientes
                if request.user.pontos < pontos_necessarios:
                    raise ValueError("Pontos insuficientes para realizar este pedido.")

                # Subtrair os pontos do cliente
                request.user.pontos -= pontos_necessarios
                request.user.save()
            else:
                # Calcular os pontos ganhos (10% do subtotal) apenas para outras formas de pagamento
                pontos_ganhos = (subtotal * Decimal('0.1')).quantize(Decimal('1'))  # Arredonda para inteiro
                # Adicionar os pontos ganhos ao saldo do usuário
                request.user.pontos += int(pontos_ganhos)
                request.user.save()

            # Criar o pedido
            pedido = Pedido.objects.create(
                user=request.user,
                endereco=data['endereco'],
                itens=data['itens'],
                subtotal=subtotal,
                total=total,
                taxa_entrega=data.get('taxa_entrega', Decimal('0')),
                taxa_cartao=data.get('taxa_cartao', Decimal('0')),
                troco=data.get('troco', None),  # O troco pode ser None, caso não seja enviado
                bairro=bairro,
                forma_pagamento=forma_pagamento,
                pontos_ganhos=pontos_ganhos  # Atribuir os pontos ganhos
            )


            return JsonResponse({
                'status': 'success',
                'pedido_id': pedido.id,
                'redirect_url': reverse('pedidos')
            }, status=201)

        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Erro interno: {str(e)}"}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

def contato(request):
    return render(request, 'contato.html')

def pix(request):
    return render(request, 'pix.html')

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def gerencia(request):
    configuracao = get_object_or_404(ConfiguracaoLoja, pk=1)
    if request.method == 'POST':
        # Atualizar o status do pedido
        pedido_id = request.POST.get('pedido_id')
        novo_status = request.POST.get('status')
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.status = novo_status
        pedido.save()

        return JsonResponse({'status': 'success', 'message': 'Status atualizado com sucesso!'})
    pedidos = Pedido.objects.all().order_by('-id')
    for pedido in pedidos:
        pedido.troco_calculado = (pedido.total - (pedido.troco or 0))*-1
    return render(request, 'gerencia.html', {'pedidos': pedidos, 'configuracao':configuracao})

def marcar_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.pago=True
    pedido.save()
    return redirect('gerencia')

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


