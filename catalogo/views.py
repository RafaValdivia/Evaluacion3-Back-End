from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.db.models import Q
from .models import Videojuego
from .forms import VideojuegoForm
from django.http import JsonResponse
from .models import Videojuego 


# 1. LEER — Catálogo Público con Búsqueda y Filtro por Plataforma
def lista_videojuegos(request):
    query = request.GET.get('q', '').strip()
    plataforma_filtro = request.GET.get('plataforma', '').strip()

    juegos = Videojuego.objects.all()

    if query:
        juegos = juegos.filter(Q(titulo__icontains=query) | Q(plataforma__icontains=query))

    if plataforma_filtro:
        juegos = juegos.filter(plataforma=plataforma_filtro)

    plataformas = Videojuego.PLATAFORMA_CHOICES

    context = {
        'juegos': juegos,
        'query': query,
        'plataforma_filtro': plataforma_filtro,
        'plataformas': plataformas,
        'total_juegos': juegos.count(),
    }
    return render(request, 'catalogo/tienda.html', context)


# 2. CREAR — Solo administradores (is_staff)
@staff_member_required(login_url='login')
def crear_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST)
        if form.is_valid():
            juego = form.save()
            messages.success(request, f'¡El videojuego "{juego.titulo}" fue registrado exitosamente en el catálogo!')
            return redirect('lista_videojuegos')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario antes de guardar.')
    else:
        form = VideojuegoForm()
    return render(request, 'catalogo/crear.html', {'form': form})


# 3. EDITAR / MODIFICAR — Solo administradores
@staff_member_required(login_url='login')
def editar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, instance=juego)
        if form.is_valid():
            juego = form.save()
            messages.success(request, f'¡Los datos del videojuego "{juego.titulo}" se actualizaron correctamente!')
            return redirect('lista_videojuegos')
        else:
            messages.error(request, 'No se pudo guardar la modificación. Verifica los campos requeridos.')
    else:
        form = VideojuegoForm(instance=juego)
    return render(request, 'catalogo/editar.html', {'form': form, 'juego': juego})


# 4. ELIMINAR — Solo administradores
@staff_member_required(login_url='login')
def eliminar_videojuego(request, id):
    juego = get_object_or_404(Videojuego, id=id)
    if request.method == 'POST':
        titulo = juego.titulo
        juego.delete()
        messages.warning(request, f'El videojuego "{titulo}" ha sido eliminado del catálogo.')
        return redirect('lista_videojuegos')
    return render(request, 'catalogo/eliminar.html', {'juego': juego})


# 5. LOGOUT PERSONALIZADO CON MENSAJE FLASH
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente. Volviendo al modo visitante.')
    return redirect('lista_videojuegos')

# 6. API REST para obtener la lista de videojuegos en formato JSON
def api_lista_videojuegos(request):
    # Trae todos los registros de la base de datos MySQL
    juegos = Videojuego.objects.all().values('id', 'titulo', 'plataforma', 'stock', 'precio')
    
    # Convierte el resultado en una lista para poder enviarlo
    lista_juegos = list(juegos)
    
    # Retorna la respuesta en formato JSON nativo
    return JsonResponse(lista_juegos, safe=False, json_dumps_params={'ensure_ascii': False})

