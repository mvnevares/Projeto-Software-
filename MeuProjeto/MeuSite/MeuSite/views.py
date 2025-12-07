from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import UsuarioPerfil, Resumo, Comentario, Material, Video


# -----------------------------
# LOGIN
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('home')

        return render(request, 'MeuSite/login.html', {
            'error': 'Usuário ou senha incorretos.',
            'next': next_url
        })

    next_url = request.GET.get('next', '')
    return render(request, 'MeuSite/login.html', {'next': next_url})


# -----------------------------
# SIGNUP (cria User + perfil)
# -----------------------------
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


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# -----------------------------
# HOME
# -----------------------------
def home(request):
    return render(request, "MeuSite/home.html")


# -----------------------------
# CRIAR RESUMO
# -----------------------------
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

    return render(request, "MeuSite/criarResumo.html")  # <-- corrigido

from django.shortcuts import render
# (Assumindo que você já tem o from django.shortcuts import render no topo)

# ... (outras funções de view)

def lista_resumo_view(request):
    """
    View responsável por listar todos os resumos disponíveis.
    """
    # 1. (Opcional): Aqui você carregaria os resumos do banco de dados
    #    resumos = Resumo.objects.all()
    
    # 2. Retorna o template HTML com ou sem os dados (context)
    return render(request, 'MeuSite/listaResumo.html', {})
    # O segundo argumento (template) usa a string 'MeuSite/listaResumo.html'
    # que aponta para: MeuProjeto/MeuSite/MeuSite/templates/MeuSite/listaResumo.html
# -----------------------------
# PERFIL
# -----------------------------
def perfil_view(request, username):
    usuario = get_object_or_404(User, username=username)
    perfil = UsuarioPerfil.objects.get(user=usuario)
    resumos = Resumo.objects.filter(autor=usuario).order_by("-data_criacao")

    return render(request, "MeuSite/perfil.html", {
        "usuario": usuario,
        "perfil": perfil,
        "resumos": resumos
    })


# -----------------------------
# EDITAR PERFIL
# -----------------------------
@login_required
def editar_perfil_view(request):
    perfil = UsuarioPerfil.objects.get(user=request.user)

    if request.method == "POST":
        perfil.bio = request.POST.get("bio")
        perfil.area_estudo = request.POST.get("area_estudo")

        if "foto" in request.FILES:
            perfil.foto = request.FILES["foto"]

        perfil.save()

        messages.success(request, "Perfil atualizado!")
        return redirect("perfil", username=request.user.username)

    return render(request, "MeuSite/editarPerfil.html")  # <-- corrigido


# -----------------------------
# GRUPOS
# -----------------------------
def grupos_view(request):
    return render(request, "MeuSite/grupos.html")


def criar_grupo_view(request):
    return render(request, "MeuSite/criarGrupo.html")  # <-- corrigido


# -----------------------------
# BATALHAS
# -----------------------------
def batalha_view(request):
    return render(request, "MeuSite/batalha.html")  # <-- corrigido


def votar_batalha_view(request, batalha_id, escolha):
    return render(request, "MeuSite/batalha.html")  # (ajuste se tiver outro template)


# -----------------------------
# UPLOAD VÍDEOS
# -----------------------------
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


# -----------------------------
# LISTA DE VÍDEOS
# -----------------------------
def pagina_video_view(request):
    videos = Video.objects.all().order_by("-criado_em")
    return render(request, "MeuSite/paginaVideo.html", {"videos": videos})  # <-- corrigido
