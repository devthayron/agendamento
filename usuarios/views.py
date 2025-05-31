from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

# verifica se o usuário está logado e se é 'gerente'
def is_gerente(user):
    return user.is_authenticated and user.is_gerente

User = get_user_model()

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()  
            messages.success(request, f'Usuário {usuario} cadastrado com sucesso.')
            return redirect('listar_usuarios')    
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registrar.html', {'form': form})


@login_required
@user_passes_test(is_gerente)
def desativar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.user.id != user.id:
        user.is_active = False
        user.save()
        messages.warning(request, f'Usuário {user} desativado com sucesso.')
    else:
        messages.error(request, 'Você não pode desativar seu próprio usuário.')
    return redirect('listar_usuarios')

@login_required
@user_passes_test(is_gerente)
def reativar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'Usuário {user} reativado com sucesso.')
    return redirect('listar_usuarios')

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            
            login(request, usuario)
            return redirect('agendamento_criar')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('login')


@login_required
@user_passes_test(lambda u: u.is_gerente)
def listar_usuarios(request):
    usuarios = User.objects.all()

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/gerenciar_usuarios.html', {
        'form': form,
        'usuarios': usuarios
    })

@login_required
@user_passes_test(lambda u: u.is_gerente)
def excluir_usuario(request, usuario_id):
    usuario = User.objects.get(id=usuario_id)
    if request.method == 'POST':
        if request.user.id != usuario_id:  # impede deletar a si mesmo
            usuario.delete()
            messages.error(request, 'Usuário excluido com sucesso.')
            return redirect('listar_usuarios')

    return render(request, 'usuarios/confirm_delete.html', {'usuario': usuario})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('agendamento_criar')
        else:
            erro = "Usuário ou senha inválidos."
            return render(request, 'usuarios/login.html', {'erro': erro})
    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
