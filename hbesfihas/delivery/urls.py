from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from . views import gerar_pix_qrcode_view, criar_pedido

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.entrada_view, name='login'), 
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('criar_pedido/', views.criar_pedido, name='criar_pedido'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('gerar_pix_qrcode/', gerar_pix_qrcode_view, name='gerar_pix_qrcode'),
    path('contato', views.contato, name='contato')
]
