from django.db import models


class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return f"{self.titulo} ({self.plataforma}) - ${self.precio}"
