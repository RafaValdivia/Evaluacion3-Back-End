from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.lista_videojuegos, name='lista_videojuegos'),

    # Acceso de administrador
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_videojuegos'), name='logout'),

    # Gestión de inventario (solo admin)
    path('crear/', views.crear_videojuego, name='crear_videojuego'),
    path('editar/<int:id>/', views.editar_videojuego, name='editar_videojuego'),
    path('eliminar/<int:id>/', views.eliminar_videojuego, name='eliminar_videojuego'),
]
