from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
]