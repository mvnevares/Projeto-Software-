from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from MeuSite import views  # <-- MANTER SÓ ESTE

urlpatterns = [
    path("admin/", admin.site.urls),

    # Páginas principais
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),

    # Recuperação de senha
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="MeuSite/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="MeuSite/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="MeuSite/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="MeuSite/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # (Troca de senha)
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="MeuSite/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="MeuSite/password_change_done.html"
        ),
        name="password_change_done",
    ),

    # Resumos
    path("criar-resumo/", views.criar_resumo_view, name="criar_resumo"),
    path("lista-resumos/", views.lista_resumo_view, name="listaResumo"),

    # Perfil
    path("perfil/<str:username>/", views.perfil_view, name="perfil"),
    path("editar-perfil/", views.editar_perfil_view, name="editar_perfil"),

    # Grupos
    path("grupos/", views.grupos_view, name="grupos"),
    path("criar-grupo/", views.criar_grupo_view, name="criar_grupo"),

    # Batalhas
    path("batalhas/", views.batalha_view, name="batalha"),
    path(
        "batalhas/<int:batalha_id>/votar/<str:escolha>/",
        views.votar_batalha_view,
        name="votar_batalha"
    ),

    # Vídeos
    path("upload-video/", views.upload_video_view, name="upload_video"),
    path("videos/", views.pagina_video_view, name="pagina_video"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
