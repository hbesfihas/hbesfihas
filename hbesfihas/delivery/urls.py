from django.urls import path
from . import views
from .views import PedidoListView, PedidoCreateView

urlpatterns = [
    path('', views.home, name='home'),
    path('pedidos/', PedidoListView.as_view(), name='lista_pedidos'), 
    path('pedidos/criar', PedidoCreateView.as_view(), name='criar_pedido'), 
    path('processa-pedido/', views.processa_pedido, name='processa_pedido'),
]