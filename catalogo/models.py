from decimal import Decimal
from django.db import models
# Se incluye MaxValueValidator para el control del límite superior
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Videojuego(models.Model):
    PLATAFORMA_CHOICES = [
        ('PS5', 'PlayStation 5'),
        ('PS4', 'PlayStation 4'),
        ('Xbox Series X', 'Xbox Series X/S'),
        ('Nintendo Switch', 'Nintendo Switch'),
        ('PC', 'PC Master Race'),
        ('Otro', 'Otra Plataforma'),
    ]

    titulo = models.CharField(
        max_length=100, 
        verbose_name="Título del videojuego",
        help_text="Nombre completo del videojuego"
    )
    plataforma = models.CharField(
        max_length=50, 
        choices=PLATAFORMA_CHOICES,
        default='PS5',
        verbose_name="Plataforma"
    )
    
    # Límite máximo de precio: $250.000 CLP (hasta 6 dígitos)
    precio = models.IntegerField(
        validators=[
            MinValueValidator(1, message="El precio debe ser al menos de $1 CLP."),
            MaxValueValidator(250000, message="El precio no puede superar los $250.000 CLP.")
        ],
        verbose_name="Precio (CLP)"
    )
    
    # Límite máximo de stock: 100 unidades (hasta 3 dígitos)
    stock = models.IntegerField(
        default=0, 
        validators=[
            MinValueValidator(0, message="El stock no puede ser negativo."),
            MaxValueValidator(100, message="El stock no puede superar las 100 unidades.")
        ],
        verbose_name="Stock disponible"
    )
    fecha_registro = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Fecha de registro"
    )

    class Meta:
        verbose_name = "Videojuego"
        verbose_name_plural = "Videojuegos"
        ordering = ['titulo']

    def __str__(self):
        return f"{self.titulo} ({self.plataforma}) - ${self.precio}"
