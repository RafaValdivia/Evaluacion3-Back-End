from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Videojuego
from .forms import VideojuegoForm


class VideojuegoModelTest(TestCase):
    def setUp(self):
        self.juego = Videojuego.objects.create(
            titulo="Super Mario Odyssey",
            plataforma="Nintendo Switch",
            precio=Decimal("49990.00"),
            stock=10
        )

    def test_str_representation(self):
        self.assertEqual(str(self.juego), "Super Mario Odyssey (Nintendo Switch) - $49990.00")


class VideojuegoValidationTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'titulo': 'God of War Ragnarök',
            'plataforma': 'PS5',
            'precio': 54990,
            'stock': 8
        }
        form = VideojuegoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_price(self):
        form_data = {
            'titulo': 'Juego Gratis Invalido',
            'plataforma': 'PC',
            'precio': -500,
            'stock': 5
        }
        form = VideojuegoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_form_invalid_stock(self):
        form_data = {
            'titulo': 'Juego Stock Invalido',
            'plataforma': 'PS5',
            'precio': 29990,
            'stock': -2
        }
        form = VideojuegoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_form_blank_title(self):
        form_data = {
            'titulo': '   ',
            'plataforma': 'PS5',
            'precio': 29990,
            'stock': 5
        }
        form = VideojuegoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)


class ViewsAccessControlTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='admin_test',
            password='password123',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='cliente_test',
            password='password123',
            is_staff=False
        )
        self.juego = Videojuego.objects.create(
            titulo="Halo Infinite",
            plataforma="Xbox Series X",
            precio=Decimal("39990.00"),
            stock=5
        )

    def test_public_catalogue_accessible(self):
        response = self.client.get(reverse('lista_videojuegos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Halo Infinite")

    def test_protected_create_redirects_anonymous(self):
        response = self.client.get(reverse('crear_videojuego'))
        self.assertEqual(response.status_code, 302)

    def test_protected_create_accessible_by_staff(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('crear_videojuego'))
        self.assertEqual(response.status_code, 200)

    def test_staff_can_create_videojuego(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.post(reverse('crear_videojuego'), {
            'titulo': 'FC 24',
            'plataforma': 'PS5',
            'precio': 49990,
            'stock': 20
        })
        self.assertRedirects(response, reverse('lista_videojuegos'))
        self.assertTrue(Videojuego.objects.filter(titulo='FC 24').exists())

    def test_staff_can_delete_videojuego(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.post(reverse('eliminar_videojuego', args=[self.juego.id]))
        self.assertRedirects(response, reverse('lista_videojuegos'))
        self.assertFalse(Videojuego.objects.filter(id=self.juego.id).exists())
