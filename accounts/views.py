from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.WARNING, 'Usuario ou senha invalidos ')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Usuario logado com sucesso')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not usuario or not email or not senha or not senha2:
        messages.add_message(request, messages.WARNING, 'Campos nao podem ficar vazio')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.WARNING, 'Email invalido')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.add_message(request, messages.WARNING, 'Senha precisa ter mais de 6 digitos')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.add_message(request, messages.WARNING, 'Usuario precisa ter mais de 6 digitos')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.add_message(request, messages.WARNING, 'Senhas precisao ser iguais')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.WARNING, 'Usuario ja existe')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.WARNING, 'Email ja existe')
        return render(request, 'accounts/cadastro.html')

    messages.add_message(request, messages.SUCCESS, 'Registrado com sucesso')

    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.add_message(request, messages.ERROR, 'Erro ao enviar formulario')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descrinao = request.POST.get('descrinao')

    if len(descrinao) < 5:
        messages.add_message(request, messages.ERROR, 'Descricao precisa ter mais que 5 caracteres')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.add_message(request, messages.SUCCESS, f'Contato {request.POST.get("nome")} cadastrado')
    return redirect('dashboard')
