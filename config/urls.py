
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from libros.views import LogoutSeguroView


urlpatterns = [
    # Panel de administración
    path("admin/", admin.site.urls),

    # Inicio de sesión
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    # Cierre de sesión seguro
    path(
        "logout/",
        LogoutSeguroView.as_view(),
        name="logout",
    ),

    # Rutas del CRUD
    path("", include("libros.urls")),
]
