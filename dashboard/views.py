from django.shortcuts import render
from agendamentos.models import Agendamento
from django.contrib.auth.decorators import login_required, user_passes_test

def is_gerente(user):
    return user.is_authenticated and user.is_gerente

@login_required
@user_passes_test(is_gerente)
def painel_dashboard(request):
    total = Agendamento.objects.count()
    pendentes = Agendamento.objects.filter(status='pendente').count()
    confirmados = Agendamento.objects.filter(status='confirmado').count()
    cancelados = Agendamento.objects.filter(status='cancelado').count()
    finalizados = Agendamento.objects.filter(status='finalizado').count()
    
    context = {
        'total': total,
        'pendentes': pendentes,
        'confirmados': confirmados,
        'cancelados': cancelados,
        'finalizados': finalizados,
    }
    return render(request, 'agendamento/dashboard.html', context)
