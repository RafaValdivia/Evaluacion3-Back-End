from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
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
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('1.00'))],
        verbose_name="Precio (CLP)"
    )
    stock = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
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
