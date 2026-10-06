from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Videojuego
from .forms import VideojuegoForm


# 1. LEER — vista pública, cualquier visitante puede ver el catálogo.
# El propio template decide qué botones mostrar según request.user.is_staff.
def lista_videojuegos(request):
    juegos = Videojuego.objects.all()
    return render(request, 'catalogo/tienda.html', {'juegos': juegos})


# 2. CREAR — solo administradores (is_staff). Si no ha iniciado sesión,
# se le redirige al login definido en LOGIN_URL.
@staff_member_required(login_url='login')
def crear_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_videojuegos')
    else:
        form = VideojuegoForm()
    return render(request, 'catalogo/crear.html', {'form': form})


# 3. MODIFICAR / EDITAR — solo administradores.
@staff_member_required(login_url='login')
def editar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, instance=juego)
        if form.is_valid():
            form.save()
            return redirect('lista_videojuegos')
    else:
        form = VideojuegoForm(instance=juego)
    return render(request, 'catalogo/editar.html', {'form': form, 'juego': juego})


# 4. ELIMINAR — solo administradores.
@staff_member_required(login_url='login')
def eliminar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    if request.method == 'POST':
        juego.delete()
        return redirect('lista_videojuegos')
    return render(request, 'catalogo/eliminar.html', {'juego': juego})
