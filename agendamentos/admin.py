from django.contrib import admin

from django.contrib import admin
from .models import Agendamento, AgendamentoProduto

# Registro do AgendamentoProduto
class AgendamentoProdutoInline(admin.TabularInline):
    model = AgendamentoProduto
    extra = 1  # Mostra um campo extra para adicionar novos produtos

# Registro do Agendamento
class AgendamentoAdmin(admin.ModelAdmin):
    inlines = [AgendamentoProdutoInline]  # Inclui os produtos dentro da tela de agendamento
    list_display = ('id', 'usuario', 'data_hora', 'status')  # Campos que aparecem na listagem do admin

admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(AgendamentoProduto)  # Registra o modelo AgendamentoProduto
