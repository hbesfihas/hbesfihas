from django.contrib import admin
from .models import Produto, Pedido, Bairro, User, Categoria
from django.utils.html import format_html

admin.site.register(Categoria),
admin.site.register(Produto),
admin.site.register(Pedido),
admin.site.register(User),
admin.site.register(Bairro),


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco','thumbnail',)  # Colunas que aparecerão na lista de sabores
    search_fields = ('nome', 'descricao')  # Permitindo a busca por nome ou descrição
    list_filter = ('nome', 'preco')  # Permitindo filtros no admin (ex: filtro por nome)
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'preco', 'imagem')
        }),
    )
    def thumbnail(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;"/>', obj.imagem.url)
        return "Sem imagem"
    
    thumbnail.short_description = "Imagem"

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'criado_em', 'atualizado_em')  # Colunas que aparecerão na lista de sabores
    search_fields = ('user__username', 'endereco')  # Permitindo a busca por nome ou descrição
    list_filter = ('status', 'criado_em')  # Permitindo filtros no admin (ex: filtro por nome)

class BairroAdmin(admin.ModelAdmin):
    list_display = ('')