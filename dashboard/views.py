from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from agendamentos.models import Agendamento
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import datetime

def is_gerente(user):
    return user.is_authenticated and user.is_gerente

def abreviar(nome, max_len=10):
    if len(nome) > max_len:
        return nome[:max_len-3] + '...'
    return nome

@login_required
@user_passes_test(is_gerente)
def painel_dashboard(request):
    agendamentos = Agendamento.objects.all()
    hoje = timezone.now().date()

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if data_inicio:
        try:
            data_inicio_date = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio_date)
        except ValueError:
            data_inicio = ''

    if data_fim:
        try:
            data_fim_date = datetime.strptime(data_fim, '%Y-%m-%d').date()
            agendamentos = agendamentos.filter(data_hora__date__lte=data_fim_date)
        except ValueError:
            data_fim = ''

    agendamentos_por_galpao = (
        agendamentos
        .values('galpao')
        .annotate(total=Count('id'))
        .order_by('galpao')
    )

    agendamentos_por_galpao_filtrados = [item for item in agendamentos_por_galpao if item['total'] > 0]
    labels_galpao = [abreviar(item['galpao'] or 'Não informado') for item in agendamentos_por_galpao_filtrados]
    data_galpao = [item['total'] for item in agendamentos_por_galpao_filtrados]

    agendamentos_por_dia = (
        agendamentos
        .annotate(data=TruncDate('data_hora'))
        .values('data')
        .annotate(total=Count('id'))
        .order_by('data')
    )
    labels_dia = [item['data'].strftime('%d/%m') for item in agendamentos_por_dia]
    data_dia = [item['total'] for item in agendamentos_por_dia]

    atrasados = agendamentos.filter(status='pendente', data_hora__lt=timezone.now()).count()

    total = agendamentos.count()
    pendentes = agendamentos.filter(status='pendente').count()
    confirmados = agendamentos.filter(status='confirmado').count()
    cancelados = agendamentos.filter(status='cancelado').count()
    finalizados = agendamentos.filter(status='finalizado').count()

    # Lista de cards com nome, cor bootstrap e valor para o template usar com for
    status_cards = [
        ('Total', 'primary', total),
        ('Pendentes', 'warning', pendentes),
        ('Confirmados', 'success', confirmados),
        ('Cancelados', 'danger', cancelados),
        ('Finalizados', 'info', finalizados),
        ('Atrasados', 'dark', atrasados),
    ]

    context = {
        'status_cards': status_cards,
        'data_inicio': data_inicio or '',
        'data_fim': data_fim or '',
        'labels_galpao': labels_galpao,
        'data_galpao': data_galpao,
        'labels_dia': labels_dia,
        'data_dia': data_dia,
    }
    return render(request, 'dashboard/dashboard.html', context)
