from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pedido, Produto
from .serializers import PedidoSerializer, PedidoCreateSerializer
from django.http import JsonResponse

def processa_pedido(request):
    if request.method == 'POST':

        return JsonResponse({'message': 'Pedido Processado com sucesso!'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})

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