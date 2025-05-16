from datetime import datetime
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
# from weasyprint import HTML
from .forms import AgendamentoForm
from .models import Agendamento, AgendamentoProduto
from .utils import verificar_disponibilidade

# verifica se o usuário está logado e se é 'gerente'
def is_gerente(user):
    return user.is_authenticated and user.is_gerente


# # ------------------  PDF  ------------------
# @login_required
# def baixar_agendamento_pdf(request, agendamento_id):
#     # busca o agendamento pelo ID e verifica se é do usuário.
#     agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)

#     html_string = render_to_string('agendamento/agendamento_pdf.html', {'agendamento': agendamento})
#     html = HTML(string=html_string)
#     response = HttpResponse(content_type='application/pdf')

#     # Define o nome do arquivo PDF
#     response['Content-Disposition'] = f'filename=agendamento_{agendamento.id}.pdf'

#     html.write_pdf(response)
#     return response

from django.contrib.auth.models import User
from django.http import HttpResponse

def criar_superusuario_temporario(request):
    if User.objects.filter(username='admin').exists():
        return HttpResponse("Superusuário já existe.")

    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    return HttpResponse("Superusuário criado com sucesso! Usuário: admin / Senha: admin123")



# ------------------ Visualizar Agendamentos ------------------

@login_required
def painel_users_list(request):
    # Filtra os agendamentos do usuário logado e ordena por data mais recente
    agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data_hora')

    # Ajusta o número de agendamentos por página
    paginator = Paginator(agendamentos, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'agendamento/painel_user.html', {'page_obj': page_obj, 'agendamentos': agendamentos})


# ------------------ Criar Agendamento ------------------
@login_required
def agendamento_criar(request):
    mensagem_erro = None
    sugestoes = None

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            galpao = form.cleaned_data['galpao']
            data_hora = form.cleaned_data['data_hora']

            # Verificação de disponibilidade antes de salvar
            disponivel, resultado = verificar_disponibilidade(galpao, data_hora.date())

            if not disponivel:
                mensagem_erro = resultado['mensagem']
                sugestoes = {
                    'anterior': resultado['anterior'],
                    'posterior': resultado['posterior'],
                }
            else:
                agendamento = form.save(commit=False)
                agendamento.usuario = request.user
                agendamento.save()

                produtos = []
                i = 0
                while True:
                    nome = request.POST.get(f'produtos[{i}][nome]')
                    quantidade = request.POST.get(f'produtos[{i}][quantidade]')
                    cubagem = request.POST.get(f'produtos[{i}][cubagem]')
                    if not nome:
                        break
                    try:
                        quantidade = float(quantidade)
                        cubagem = float(cubagem)
                    except ValueError:
                        quantidade = 0.0
                        cubagem = 0.0
                    produtos.append((nome, quantidade, cubagem))
                    i += 1

                for nome, quantidade, cubagem in produtos:
                    AgendamentoProduto.objects.create(
                        agendamento=agendamento,
                        mercadoria=nome,
                        quantidade=quantidade,
                        cubagem=cubagem
                    )
                return redirect('agendamento_criar')
    else:
        form = AgendamentoForm()

    return render(
        request,
        'agendamento/agendamento_criar.html',
        {
            'form': form,
            'mensagem_erro': mensagem_erro,
            'sugestoes': sugestoes
        }
    )


# ------------------ Editar Agendamento ------------------
@login_required
def agendamento_editar(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)

    mensagem_erro = None
    sugestoes = None

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            galpao = form.cleaned_data['galpao']
            data_hora = form.cleaned_data['data_hora']

            # Verificação de disponibilidade antes de salvar
            disponivel, resultado = verificar_disponibilidade(galpao, data_hora.date(), agendamento_id=agendamento.id)

            if not disponivel:
                mensagem_erro = resultado['mensagem']
                sugestoes = {
                    'anterior': resultado['anterior'],
                    'posterior': resultado['posterior'],
                }
            else:
                agendamento = form.save()

                produtos = []
                i = 0
                while True:
                    nome = request.POST.get(f'produtos[{i}][nome]')
                    quantidade = request.POST.get(f'produtos[{i}][quantidade]')
                    cubagem = request.POST.get(f'produtos[{i}][cubagem]')
                    if not nome:
                        break
                    try:
                        quantidade = float(quantidade)
                        cubagem = float(cubagem)
                    except ValueError:
                        quantidade = 0.0
                        cubagem = 0.0
                    produtos.append((nome, quantidade, cubagem))
                    i += 1

                # Limpa produtos antigos e salva os novos
                agendamento.itens.all().delete()
                for nome, quantidade, cubagem in produtos:
                    AgendamentoProduto.objects.create(
                        agendamento=agendamento,
                        mercadoria=nome,
                        quantidade=quantidade,
                        cubagem=cubagem
                    )

                if request.user.is_gerente:
                    return redirect('painel_gerente')
                else:
                    return redirect('painel_user')
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(
        request,
        'agendamento/agendamento_editar.html',
        {
            'form': form,
            'agendamento': agendamento,
            'mensagem_erro': mensagem_erro,
            'sugestoes': sugestoes
        }
    )



# ------------------ GERENTE: Painel ------------------
@login_required
@user_passes_test(is_gerente)
def painel_gerente(request):
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    status = request.GET.get('status')
    mercadoria = request.GET.get('mercadoria')

    agendamentos = Agendamento.objects.all()

    if data_inicial:
        try:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
            agendamentos = agendamentos.filter(data_hora__gte=data_inicial)
        except ValueError:
            pass

    if data_final:
        try:
            data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
            agendamentos = agendamentos.filter(data_hora__lte=data_final)
        except ValueError:
            pass


    if status:
        agendamentos = agendamentos.filter(status=status)

    if mercadoria:
        agendamentos = agendamentos.filter(itens__mercadoria__icontains=mercadoria).distinct()

    agendamentos = agendamentos.order_by('-data_hora')
    paginator = Paginator(agendamentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'mercadoria': mercadoria,
        'status':status,
        'status_choices':Agendamento.STATUS_CHOICES,
        'mercadoria': mercadoria,
    }

    return render(request, 'agendamento/painel_gerente.html', context)

# ------------------ GERENTE: Ações ------------------
@login_required
@user_passes_test(is_gerente)
def cancelar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    agendamento.status = 'cancelado'
    agendamento.save()
    return redirect('painel_gerente')

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


# ------------------ GERENTE: Exportação CSV ------------------
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
