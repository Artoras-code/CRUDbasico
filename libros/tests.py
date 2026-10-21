from datetime import date

from django.test import TestCase
from django.urls import reverse

from .forms import LibroForm
from .models import Libro


def datos(**cambios):
    """Datos válidos base; cada test cambia solo el campo que quiere probar."""
    base = {
        "titulo": "Cien años de soledad",
        "anio_publicacion": 1967,
        "isbn": "978-0307474728",
        "estado": "disponible",
    }
    base.update(cambios)
    return base


class ValidacionAnioTests(TestCase):
    """Campo 1: anio_publicacion (entero entre 1500 y el año actual)."""

    def test_caso1_anio_dentro_del_rango_se_acepta(self):
        self.assertTrue(LibroForm(datos(anio_publicacion=1967)).is_valid())

    def test_caso2_anio_bajo_el_minimo_se_rechaza(self):
        f = LibroForm(datos(anio_publicacion=1499))
        self.assertFalse(f.is_valid())
        self.assertIn("anio_publicacion", f.errors)

    def test_caso3_anio_minimo_exacto_se_acepta(self):
        self.assertTrue(LibroForm(datos(anio_publicacion=1500)).is_valid())

    def test_caso3b_anio_maximo_exacto_se_acepta_y_el_siguiente_no(self):
        actual = date.today().year
        self.assertTrue(LibroForm(datos(anio_publicacion=actual)).is_valid())
        self.assertFalse(LibroForm(datos(anio_publicacion=actual + 1)).is_valid())


class ValidacionIsbnTests(TestCase):
    """Campo 2: isbn (obligatorio, 10 o 13 dígitos, guiones permitidos)."""

    def test_caso4_isbn_legitimo_se_acepta(self):
        f = LibroForm(datos(isbn="978-0307474728"))
        self.assertTrue(f.is_valid())
        self.assertEqual(f.cleaned_data["isbn"], "9780307474728")

    def test_caso5a_isbn_faltante_se_rechaza(self):
        f = LibroForm(datos(isbn=""))
        self.assertFalse(f.is_valid())
        self.assertIn("isbn", f.errors)

    def test_caso5b_isbn_con_letras_se_rechaza(self):
        f = LibroForm(datos(isbn="97803074ABCDE"))
        self.assertFalse(f.is_valid())
        self.assertIn("isbn", f.errors)

    def test_caso6_isbn_frontera_10_acepta_y_9_o_12_rechaza(self):
        self.assertTrue(LibroForm(datos(isbn="0306406152")).is_valid())    # 10 dígitos
        self.assertFalse(LibroForm(datos(isbn="030640615")).is_valid())    # 9 dígitos
        self.assertFalse(LibroForm(datos(isbn="978030747472")).is_valid()) # 12 dígitos


class VistaBackendTests(TestCase):
    """Validación en el servidor sin navegador: se envía el POST directo a la vista."""

    def test_post_invalido_no_guarda_nada(self):
        resp = self.client.post(
            reverse("libro_create"), datos(anio_publicacion=1499, isbn="123")
        )
        self.assertEqual(resp.status_code, 200) 
        self.assertEqual(Libro.objects.count(), 0)

    def test_post_valido_guarda_y_redirige(self):
        resp = self.client.post(reverse("libro_create"), datos())
        self.assertRedirects(resp, reverse("libro_list"))
        self.assertEqual(Libro.objects.count(), 1)