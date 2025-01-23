from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.entrada_view, name='login'), 
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('criar_pedido/', views.criar_pedido, name='criar_pedido'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('gerencia/', views.gerencia, name='gerencia'),
    path('contato', views.contato, name='contato'),
    path('pix', views.pix, name='pix'),
    path('alterar_status/<int:pedido_id>/', views.alterar_status, name='alterar_status'),
    path('atualizar_pedidos/', views.atualizar_pedidos, name='atualizar_pedidos'),
    path('marcar_pago/<int:pedido_id>/', views.marcar_pago, name='marcar_pago'),
]
