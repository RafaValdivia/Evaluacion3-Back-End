from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.lista_videojuegos, name='lista_videojuegos'),

    # Acceso de administrador / Autenticación
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Gestión de inventario (solo admin)
    path('crear/', views.crear_videojuego, name='crear_videojuego'),
    path('editar/<int:id>/', views.editar_videojuego, name='editar_videojuego'),
    path('eliminar/<int:id>/', views.eliminar_videojuego, name='eliminar_videojuego'),
    # api de videojuegos
    path('api/videojuegos/', views.api_lista_videojuegos, name='api_videojuegos'),
]

