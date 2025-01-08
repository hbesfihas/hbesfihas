from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from . views import criar_pedido, gerencia, gerar_pix, alterar_status

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.entrada_view, name='login'), 
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('criar_pedido/', views.criar_pedido, name='criar_pedido'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('gerencia/', gerencia, name='gerencia'),
    path('contato', views.contato, name='contato'),
    path('gerar_pix', views.gerar_pix, name='gerar_pix'),
    path('alterar_status/<int:pedido_id>/', views.alterar_status, name='alterar_status'),
    path('atualizar_pedidos/', views.atualizar_pedidos, name='atualizar_pedidos'),

]
