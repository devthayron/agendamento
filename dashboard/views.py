from django.shortcuts import render
from agendamentos.models import Agendamento
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import datetime

def is_gerente(user):
    return user.is_authenticated and user.is_gerente


# ------------------ GERENTE: Dashboard ------------------
@login_required
@user_passes_test(is_gerente)
def painel_dashboard(request):
    agendamentos = Agendamento.objects.all()
    hoje = timezone.now().date()

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if data_inicio and data_fim:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        agendamentos = agendamentos.filter(data_hora__date__range=[data_inicio, data_fim])

    context = {
        'total': agendamentos.count(),
        'pendentes': agendamentos.filter(status='pendente').count(),
        'confirmados': agendamentos.filter(status='confirmado').count(),
        'cancelados': agendamentos.filter(status='cancelado').count(),
        'finalizados': agendamentos.filter(status='finalizado').count(),
        'agendamentos_hoje': agendamentos.filter(data_hora__date=hoje).count(),
        'data_inicio': data_inicio or '',
        'data_fim': data_fim or '',
    }
    return render(request, 'dashboard/dashboard.html', context)

