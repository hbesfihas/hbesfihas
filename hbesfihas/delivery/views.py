from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pedido, Produto, Bairro
from .serializers import PedidoSerializer, PedidoCreateSerializer
from .forms import PedidoForm, ItemPedidoForm
from json import dumps
from django.http import JsonResponse
from escpos.printer import Usb

def home(request):
    produtos = Produto.objects.all()
    bairros = Bairro.objects.all()
    return render(request, 'home.html', {'produtos': produtos, 'bairros': bairros})

class PedidoListView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)
    

class PedidoCreateView(APIView):
    def post(self, request):
        serializer = PedidoCreateSerializer(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()
            return Response(
                {"message": "Pedido criado com Sucesso!", "pedido_id": pedido.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def finalizar_pedido(request):
    if request.method == "POST":
        bairro_id = request.POST.get('bairro')
        forma_pagamento = request.POST.get('forma_pagamento')
        subtotal = request.POST.get('subtotal')

        # Recuperar o bairro a partir do ID
        bairro = Bairro.objects.get(id=bairro_id)

        # Processar a lógica de pagamento, salvar o pedido, etc.
        # Exemplo: Pedido.objects.create(bairro=bairro, forma_pagamento=forma_pagamento, subtotal=subtotal)

        return redirect('sucesso')  # Redirecionar para uma página de sucesso ou confirmação

def preparar_texto_impressao(pedido):
    texto = "====== HB Esfihas ======\n"
    texto += "Pedido realizado em: {}\n".format(pedido.data.strftime('%d/%m/%Y %H:%M'))
    texto += "-------------------------\n"
    texto += "Itens:\n"
    for item in pedido.itens.all():
        texto += "{}x {} - R$ {:.2f}\n".format(item.quantidade, item.produto.nome, item.total)
    texto += "-------------------------\n"
    texto += "Subtotal: R$ {:.2f}\n".format(pedido.subtotal)
    texto += "Taxa de entrega: R$ {:.2f}\n".format(pedido.taxa_entrega)
    texto += "Total: R$ {:.2f}\n".format(pedido.total)
    texto += "-------------------------\n"
    texto += "Forma de pagamento: {}\n".format(pedido.forma_pagamento)
    texto += "Observações:\n{}\n".format(pedido.observacoes or "Nenhuma")
    texto += "=========================\n"
    texto += "Obrigado pela preferência!"
    return texto
def imprimir_pedido(request):
    if request.method == "POST":
        dados = json.loads(request.body)
        try:
            texto_impressao = "====== HB Esfihas ======\n"
            texto_impressao += "Itens do Pedido:\n"
            for item in dados["itens"]:
                texto_impressao += f"{item['quantidade']}x {item['nome']} - R$ {item['preco']:.2f}\n"
            texto_impressao += "-------------------------\n"
            texto_impressao += f"Subtotal: R$ {dados['subtotal']}\n"
            texto_impressao += f"Taxa de entrega: R$ {dados['taxa_entrega']}\n"
            texto_impressao += f"Total: R$ {dados['total']}\n"
            texto_impressao += f"Forma de pagamento: {dados['forma_pagamento']}\n"
            texto_impressao += "=========================\n"
            texto_impressao += "Obrigado pela preferência!\n"

            # Configurar a impressora USB
            printer = Usb(0x28E9, 0x0289)  # Substitua pelos valores corretos
            printer.text(texto_impressao)
            printer.cut()

            return JsonResponse({"status": "success"})
        except Exception as e:
            print("Erro ao imprimir:", e)
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Método não permitido"}, status=405)

