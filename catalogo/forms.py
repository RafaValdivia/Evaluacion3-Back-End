from decimal import Decimal
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Videojuego


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Usuario o contraseña incorrectos. Por favor, verifica tus credenciales e inténtalo nuevamente.",
        'inactive': "Esta cuenta se encuentra desactivada.",
    }

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
                'placeholder': 'Ej: Elden Ring: Shadow of the Erdtree',
            }),
            'plataforma': forms.Select(attrs={
                'class': 'form-select',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'min': '1',
                'max': '250000',
                'maxlength': '6',
                'oninput': "if(this.value.length > 6) this.value = this.value.slice(0, 6);",
                'placeholder': 'Ej: 59990',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'maxlength': '3',
                'oninput': "if(this.value.length > 3) this.value = this.value.slice(0, 3);",
                'placeholder': 'Ej: 15',
            }),
        }
        labels = {
            'titulo': 'Título del Videojuego',
            'plataforma': 'Plataforma / Consola',
            'precio': 'Precio (CLP)',
            'stock': 'Stock disponible',
        }
        help_texts = {
            'precio': 'Ingrese el valor monetario en pesos chilenos (máximo $250.000 y hasta 6 dígitos).',
            'stock': 'Unidades en bodega disponibles para venta (máximo 100 y hasta 3 dígitos).',
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if not titulo:
            raise forms.ValidationError("El título del videojuego es obligatorio y no puede contener solo espacios.")
        if len(titulo) < 2:
            raise forms.ValidationError("El título del videojuego debe tener al menos 2 caracteres.")
        return titulo

    def clean_plataforma(self):
        plataforma = self.cleaned_data.get('plataforma')
        if not plataforma:
            raise forms.ValidationError("Debe seleccionar una plataforma válida.")
        return plataforma

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None:
            raise forms.ValidationError("El precio es obligatorio.")
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser un valor positivo estrictamente mayor que cero.")
        if len(str(abs(int(precio)))) > 6:
            raise forms.ValidationError("El precio no puede tener más de 6 dígitos.")
        if precio > 250000:
            raise forms.ValidationError("El precio no puede superar los $250.000 CLP.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None:
            raise forms.ValidationError("El stock es un campo obligatorio.")
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser un valor negativo.")
        if len(str(abs(int(stock)))) > 3:
            raise forms.ValidationError("La cantidad no puede tener más de 3 dígitos.")
        if stock > 100:
            raise forms.ValidationError("La cantidad máxima de stock no puede superar las 100 unidades.")
        return stock
