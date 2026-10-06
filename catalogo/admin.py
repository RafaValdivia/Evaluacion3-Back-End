from django.contrib import admin
from .models import Videojuego


@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'plataforma', 'precio', 'stock')
    list_filter = ('plataforma',)
    search_fields = ('titulo',)
