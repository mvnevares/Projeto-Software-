from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UsuarioPerfil, Resumo, Video
from MeuSite.models import Resumo
from django.conf import settings 
from MeuSite import views

def sobre_view(request):
    return render(request, 'MeuSite/sobre.html', {})

def home_view(request): 
    return render(request, 'MeuSite/home.html', {})

def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return redirect(settings.LOGIN_REDIRECT_URL) 
        else:
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
            return render(request, 'MeuSite/login.html', {})
    return render(request, 'MeuSite/login.html', {})

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        if password != confirm:
            messages.error(request, "As senhas não coincidem.")
            return redirect("signup")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe.")
            return redirect("signup")
        user = User.objects.create_user(username=username, email=email, password=password)
        UsuarioPerfil.objects.create(user=user)
        login(request, user)
        return redirect("home")
    return render(request, "MeuSite/signup.html")

def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL) 

def termos_view(request):
    return render(request, 'MeuSite/termos.html', {})

def colaboradores_view(request):
    return render(request, 'MeuSite/colaboradores.html', {})

@login_required
def criar_resumo_view(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        materia = request.POST.get("materia")
        conteudo = request.POST.get("conteudo")
        Resumo.objects.create(
            titulo=titulo,
            materia=materia,
            conteudo=conteudo,
            autor=request.user
        )
        messages.success(request, "Resumo criado com sucesso!")
        return redirect("home")
    return render(request, "MeuSite/criarResumo.html")  

@login_required
def busca_resumo_view(request):
    context = {
        'termo_busca': ''
    }
    return render(request, 'MeuSite/buscaResumo.html', context)

@login_required
def lista_resumo_view(request):
    resumos = Resumo.objects.all()
    return render(request, 'MeuSite/listaResumo.html', {})

@login_required
def ver_resumo_view(request, resumo_id):
    resumo = get_object_or_404(Resumo, id=resumo_id)
    context = {
        'resumo': resumo,
    }
    return render(request, 'MeuSite/verResumo.html', context)

@login_required
def perfil_view(request, username):
    user = get_object_or_404(User, username=username)
    try:
        perfil = user.usuarioperfil
    except UsuarioPerfil.DoesNotExist:
        perfil = UsuarioPerfil.objects.create(user=user)
    resumos = Resumo.objects.filter(autor=user).order_by("-data_criacao")
    context = {
        'user_page': user,
        'perfil': perfil,
        # ...
    }
    return render(request, "MeuSite/perfil.html", {
        "usuario": user,
        "perfil": perfil,
        "resumos": resumos
    })

@login_required
@login_required
def editar_perfil_view(request):
    try:
        perfil = UsuarioPerfil.objects.get(user=request.user)
    except UsuarioPerfil.DoesNotExist:
        perfil = UsuarioPerfil.objects.create(user=request.user)
        
    if request.method == "POST":
        try:
            # 1. Atribuição e salvamento dos campos do Perfil
            perfil.bio = request.POST.get("bio")
            perfil.area_estudo = request.POST.get("area_estudo")
            
            if "foto" in request.FILES:
                perfil.foto = request.FILES["foto"]
            
            perfil.save()
            
            # 2. Atribuição e salvamento do nome (campo first_name do User)
            nome_digitado = request.POST.get("display_name")
            if nome_digitado:
                request.user.first_name = nome_digitado 
                request.user.save()
            
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("perfil", username=request.user.username)
            
        except Exception as e:
            messages.error(request, f"Erro ao salvar: {e}. Verifique os dados.")
            
    context = {
        'perfil': perfil, 
        'user': request.user
    }
    return render(request, "MeuSite/editarPerfil.html", context)
    

@login_required
def grupos_view(request):
    return render(request, "MeuSite/grupos.html")

@login_required
def criar_grupo_view(request):
    return render(request, "MeuSite/criarGrupo.html") 
@login_required
def batalha_view(request):
    return render(request, "MeuSite/batalha.html") 
@login_required
def votar_batalha_view(request, batalha_id, escolha):
    return render(request, "MeuSite/batalha.html") 

@login_required
def upload_video_view(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        url = request.POST.get("url")
        Video.objects.create(
            titulo=titulo,
            url=url,
            autor=request.user
        )
        messages.success(request, "Vídeo enviado!")
        return redirect("pagina_video")
    return render(request, "MeuSite/uploadVideo.html")  # <-- corrigido
@login_required
def pagina_video_view(request):
    videos = Video.objects.all().order_by("-criado_em")
    return render(request, "MeuSite/paginaVideo.html", {"videos": videos})  # <-- corrigido
@login_required
def get(self, request, *args, **kwargs):
    resumos = Resumo.objects.all().order_by('-data_criacao')
    contexto = {'pessoas': resumos}       
    return render(request, 'MeuSite/listaResumos.html', contexto)