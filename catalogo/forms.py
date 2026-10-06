from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Videojuego


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario...',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })
    )


class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['titulo', 'plataforma', 'precio', 'stock']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Elden Ring',
            }),
            'plataforma': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: PS5, PC, Switch',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'min': '1',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
        }
        labels = {
            'titulo': 'Título',
            'plataforma': 'Plataforma',
            'precio': 'Precio (CLP)',
            'stock': 'Stock disponible',
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser un valor mayor que cero.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser un número negativo.")
        return stock
