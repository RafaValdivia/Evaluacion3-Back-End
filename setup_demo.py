import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TiendaDeVideojuegos.settings')
django.setup()

from django.contrib.auth.models import User
from catalogo.models import Videojuego

print("=== GamerShop Data Seeder & Admin Creator ===")

# 1. Crear Superusuario (admin / admin123)
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@gamershop.cl', 'admin123')
    print("[OK] Superusuario 'admin' creado exitosamente con contrasena 'admin123'.")
else:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("[OK] Superusuario 'admin' actualizado correctamente con contrasena 'admin123'.")

# 2. Poblar datos iniciales de prueba si la base de datos esta vacia
juegos_iniciales = [
    {
        'titulo': 'The Legend of Zelda: Tears of the Kingdom',
        'plataforma': 'Nintendo Switch',
        'precio': 59990,
        'stock': 12,
    },
    {
        'titulo': 'Elden Ring: Shadow of the Erdtree Edition',
        'plataforma': 'PS5',
        'precio': 64990,
        'stock': 8,
    },
    {
        'titulo': 'Halo Infinite',
        'plataforma': 'Xbox Series X',
        'precio': 39990,
        'stock': 15,
    },
    {
        'titulo': 'Cyberpunk 2077: Phantom Liberty',
        'plataforma': 'PC',
        'precio': 34990,
        'stock': 20,
    },
    {
        'titulo': 'God of War Ragnarok',
        'plataforma': 'PS5',
        'precio': 49990,
        'stock': 6,
    },
]

creados = 0
for data in juegos_iniciales:
    if not Videojuego.objects.filter(titulo=data['titulo']).exists():
        Videojuego.objects.create(**data)
        creados += 1

print(f"[OK] {creados} videojuegos iniciales agregados al catalogo.")
print(f"Total de registros en base de datos: {Videojuego.objects.count()}")
print("=== Proceso completado exitosamente ===")
