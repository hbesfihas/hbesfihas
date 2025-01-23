from django.contrib import admin
from .models import ConfiguracaoLoja, Produto, Pedido, Bairro, User, Categoria
from django.utils.html import format_html

admin.site.register(Categoria),
@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'taxa_entrega')
    list_editable =('taxa_entrega',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('thumbnail','nome', 'preco','disponivel','trocavel_por_pontos','pontos_troca','descricao')  # Colunas que aparecerão na lista de sabores
    list_editable = ('preco', 'disponivel', 'trocavel_por_pontos', 'pontos_troca')
    search_fields = ('nome', 'descricao')  # Permitindo a busca por nome ou descrição
    list_filter = ('disponivel','categoria')  # Permitindo filtros no admin (ex: filtro por nome)
    fieldsets = (
        (None, {
            'fields': ('categoria','nome', 'descricao', 'preco', 'imagem', 'pontos_troca')
        }),
    )
    def thumbnail(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;"/>', obj.imagem.url)
        return "Sem imagem"
    
    thumbnail.short_description = "Imagem"

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'criado_em', 'atualizado_em')  # Colunas que aparecerão na lista de sabores
    search_fields = ('user__username', 'endereco')  # Permitindo a busca por nome ou descrição
    list_filter = ('status', 'criado_em')  # Permitindo filtros no admin (ex: filtro por nome)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nome', 'whatsapp','pontos', 'is_staff', 'is_active')


@admin.register(ConfiguracaoLoja)
class ConfiguracaoLojaAdmin(admin.ModelAdmin):
    list_display = ['loja_aberta']