from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AgendamentoForm
from .models import Agendamento,AgendamentoProduto
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.db.models import Count
from datetime import datetime
import csv
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
# from .models import Agendamento
# from django.contrib.auth.decorators import login_required, user_passes_test
# from .utils import is_gerente
# from io import BytesIO

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import Agendamento

def baixar_agendamento_pdf(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id)
    html_string = render_to_string('agendamento/agendamento_pdf.html', {'agendamento': agendamento})
    html = HTML(string=html_string)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=agendamento_{agendamento.id}.pdf'
    html.write_pdf(response)
    
    return response


# usuarios
@login_required
def user_agendamentos_list(request):
    # Filtra os agendamentos do usuário logado
    agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data_hora')

    # Passa os agendamentos para o template
    return render(request, 'agendamento/meus_agendamentos.html', {'agendamentos': agendamentos})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AgendamentoForm
from .models import Agendamento, AgendamentoProduto

@login_required
def agendamento_edit(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)  # Busca o agendamento pelo ID

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)  # Preenche o formulário com os dados do agendamento
        if form.is_valid():
            agendamento = form.save()  # Salva as mudanças no agendamento

            # Coletando os produtos enviados no formato produtos[0][nome], produtos[0][quantidade], etc.
            produtos = []
            i = 0
            while True:
                nome = request.POST.get(f'produtos[{i}][nome]')
                quantidade = request.POST.get(f'produtos[{i}][quantidade]')
                cubagem = request.POST.get(f'produtos[{i}][cubagem]')
                if not nome:
                    break  # Parar se não houver mais produtos
                try:
                    quantidade = float(quantidade)
                    cubagem = float(cubagem)
                except ValueError:
                    quantidade = 0.0
                    cubagem = 0.0
                produtos.append((nome, quantidade, cubagem))
                i += 1

            # Atualizando os produtos no agendamento
            agendamento.itens.all().delete()  # Remove todos os produtos existentes
            for nome, quantidade, cubagem in produtos:
                AgendamentoProduto.objects.create(
                    agendamento=agendamento,
                    mercadoria=nome,
                    quantidade=quantidade,
                    cubagem=cubagem
                )

            return redirect('meus_agendamentos')  # Redireciona para a lista de agendamentos

    else:
        form = AgendamentoForm(instance=agendamento)  # Cria o formulário com os dados atuais do agendamento

    return render(request, 'agendamento/agendamento_edit.html', {'form': form, 'agendamento': agendamento})

@login_required
def pagina_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)

        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user
            agendamento.save()

            # Coletando todos os produtos enviados no formato produtos[0][nome], produtos[0][quantidade], etc.
            produtos = []
            i = 0
            while True:
                nome = request.POST.get(f'produtos[{i}][nome]')
                quantidade = request.POST.get(f'produtos[{i}][quantidade]')
                cubagem = request.POST.get(f'produtos[{i}][cubagem]')
                if not nome:
                    break  # Parar se não houver mais produtos
                # Convertendo quantidade e cubagem para float
                try:
                    quantidade = float(quantidade)
                    cubagem = float(cubagem)
                except ValueError:
                    quantidade = 0.0  # Definindo valor default caso falhe a conversão
                    cubagem = 0.0
                produtos.append((nome, quantidade, cubagem))
                i += 1

            # Criando os objetos AgendamentoProduto e associando ao agendamento
            for nome, quantidade, cubagem in produtos:
                AgendamentoProduto.objects.create(
                    agendamento=agendamento,
                    mercadoria=nome,
                    quantidade=quantidade,
                    cubagem=cubagem
                )

            return redirect('pagina_agendamento')

    else:
        form = AgendamentoForm()

    return render(request, 'agendamento/agendar.html', {'form': form})


def is_gerente(user):
    return user.is_authenticated and user.is_gerente

@login_required
@user_passes_test(is_gerente)
def painel_gerente(request):
    # Pega os parâmetros de data, cnpj, fornecedor e mercadoria da URL
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    cnpj = request.GET.get('cnpj')
    fornecedor = request.GET.get('fornecedor')
    mercadoria = request.GET.get('mercadoria')

    agendamentos = Agendamento.objects.all()

    # Filtra por data inicial, caso a data_inicial tenha sido fornecida
    if data_inicial:
        try:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()  # Converte para um objeto Date
            agendamentos = agendamentos.filter(data_hora__gte=data_inicial)  # Filtra por data maior ou igual
        except ValueError:
            pass  # Caso a data não tenha o formato correto, ignora

    # Filtra por data final, caso a data_final tenha sido fornecida
    if data_final:
        try:
            data_final = datetime.strptime(data_final, '%Y-%m-%d').date()  # Converte para um objeto Date
            agendamentos = agendamentos.filter(data_hora__lte=data_final)  # Filtra por data menor ou igual
        except ValueError:
            pass  # Caso a data não tenha o formato correto, ignora

    # Filtros adicionais
    if cnpj:
        agendamentos = agendamentos.filter(cnpj__icontains=cnpj)

    if fornecedor:
        agendamentos = agendamentos.filter(fornecedor__icontains=fornecedor)

    if mercadoria:
        agendamentos = agendamentos.filter(mercadoria__icontains=mercadoria)

    # Ordenando os agendamentos pela data mais recente
    agendamentos = agendamentos.order_by('-data_hora')

    # Paginação dos resultados
    paginator = Paginator(agendamentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexto para o template
    context = {
        'page_obj': page_obj,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'cnpj': cnpj,
        'fornecedor': fornecedor,
        'mercadoria': mercadoria,
    }

    return render(request, 'agendamento/painel_gerente.html', context)

@login_required
@user_passes_test(is_gerente)
def cancelar_agendamento(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id)
    agendamento.status = 'cancelado'
    agendamento.save()
    return redirect('painel_gerente')

@login_required
@user_passes_test(is_gerente)
def dashboard_gerente(request):
    agendamentos = Agendamento.objects.all()
    hoje = timezone.now().date()

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if data_inicio and data_fim:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        agendamentos = agendamentos.filter(data_hora__date__range=[data_inicio, data_fim])

    total = agendamentos.count()
    pendentes = agendamentos.filter(status='pendente').count()
    confirmados = agendamentos.filter(status='confirmado').count()
    cancelados = agendamentos.filter(status='cancelado').count()
    finalizados = agendamentos.filter(status='finalizado').count()

    agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje).count()

    context = {
        'total': total,
        'pendentes': pendentes,
        'confirmados': confirmados,
        'cancelados': cancelados,
        'agendamentos_hoje': agendamentos_hoje,
        'finalizados': finalizados,
        'data_inicio': request.GET.get('data_inicio', ''),
        'data_fim': request.GET.get('data_fim', '')
    }
    return render(request, 'agendamento/dashboard.html', context)

@login_required
@user_passes_test(is_gerente)
def confirmar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    if agendamento.status == 'pendente':
        agendamento.status = 'confirmado'
        agendamento.save()
    return redirect('painel_gerente')

@login_required
@user_passes_test(is_gerente)
def finalizar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    if agendamento.status == 'confirmado':
        agendamento.status = 'finalizado'
        agendamento.save()
    return redirect('painel_gerente')

@login_required
@user_passes_test(is_gerente)
def exportar_agendamentos_csv(request):
    agendamentos = Agendamento.objects.prefetch_related('itens').all()

    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial and data_final:
        agendamentos = agendamentos.filter(data_agendamento__range=[data_inicial, data_final])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="agendamentos.csv"'

    writer = csv.writer(response)
    # Cabeçalhos CSV
    writer.writerow([
        'Data Agendamento', 'CNPJ', 'Fornecedor', 'Email', 'Transportadora',
        'Tipo de Carga', 'Pedido', 'Nota Fiscal', 'Produto', 'Quantidade',
        'Cubagem', 'Status'
    ])

    for ag in agendamentos:
        if ag.itens.exists():
            for item in ag.itens.all():
                writer.writerow([
                    ag.data_hora.strftime('%d/%m/%Y'),
                    ag.cnpj,
                    ag.fornecedor,
                    ag.email,
                    ag.transportadora,
                    ag.tipo_carro,
                    ag.pedido,
                    ag.nota_fiscal,
                    item.mercadoria,
                    float(item.quantidade),
                    float(item.cubagem),
                    ag.get_status_display()
                ])
        else:
            # Caso não tenha produtos, linha com campos de produtos vazios
            writer.writerow([
                ag.data_hora.strftime('%d/%m/%Y'),
                ag.cnpj,
                ag.fornecedor,
                ag.email,
                ag.transportadora,
                ag.tipo_carro,
                ag.pedido,
                ag.nota_fiscal,
                '---', '', '',
                ag.get_status_display()
            ])

    return response