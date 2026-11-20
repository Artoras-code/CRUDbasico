
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from .forms import LibroForm
from .models import Libro


def datos(**cambios):
    """Datos válidos base para las pruebas."""
    base = {
        "titulo": "Cien años de soledad",
        "anio_publicacion": 1967,
        "isbn": "978-0307474728",
        "estado": "disponible",
    }
    base.update(cambios)
    return base


def crear_usuario(username, permisos=()):
    """Crea un usuario ficticio con los permisos indicados."""
    usuario = get_user_model().objects.create_user(
        username=username,
        password="ClaveTemporal-Pruebas-2026!",
    )

    for codigo in permisos:
        permiso = Permission.objects.get(
            content_type__app_label="libros",
            codename=codigo,
        )
        usuario.user_permissions.add(permiso)

    return usuario


class ValidacionAnioTests(TestCase):

    def test_caso1_anio_dentro_del_rango_se_acepta(self):
        self.assertTrue(
            LibroForm(datos(anio_publicacion=1967)).is_valid()
        )

    def test_caso2_anio_bajo_el_minimo_se_rechaza(self):
        f = LibroForm(datos(anio_publicacion=1499))
        self.assertFalse(f.is_valid())
        self.assertIn("anio_publicacion", f.errors)

    def test_caso3_anio_minimo_exacto_se_acepta(self):
        self.assertTrue(
            LibroForm(datos(anio_publicacion=1500)).is_valid()
        )

    def test_caso3b_anio_maximo_exacto_se_acepta_y_el_siguiente_no(self):
        actual = date.today().year

        self.assertTrue(
            LibroForm(datos(anio_publicacion=actual)).is_valid()
        )
        self.assertFalse(
            LibroForm(datos(anio_publicacion=actual + 1)).is_valid()
        )


class ValidacionIsbnTests(TestCase):

    def test_caso4_isbn_legitimo_se_acepta(self):
        f = LibroForm(datos(isbn="978-0307474728"))
        self.assertTrue(f.is_valid())
        self.assertEqual(
            f.cleaned_data["isbn"],
            "9780307474728",
        )

    def test_caso5a_isbn_faltante_se_rechaza(self):
        f = LibroForm(datos(isbn=""))
        self.assertFalse(f.is_valid())
        self.assertIn("isbn", f.errors)

    def test_caso5b_isbn_con_letras_se_rechaza(self):
        f = LibroForm(datos(isbn="97803074ABCDE"))
        self.assertFalse(f.is_valid())
        self.assertIn("isbn", f.errors)

    def test_caso6_isbn_frontera_10_acepta_y_9_o_12_rechaza(self):
        self.assertTrue(
            LibroForm(datos(isbn="0306406152")).is_valid()
        )
        self.assertFalse(
            LibroForm(datos(isbn="030640615")).is_valid()
        )
        self.assertFalse(
            LibroForm(datos(isbn="978030747472")).is_valid()
        )


class VistaBackendTests(TestCase):
    """Comprueba las validaciones con un usuario autorizado."""

    def setUp(self):
        self.usuario = crear_usuario(
            "editor_prueba",
            permisos=("view_libro", "add_libro"),
        )
        self.client.force_login(self.usuario)

    def test_post_invalido_no_guarda_nada(self):
        resp = self.client.post(
            reverse("libro_create"),
            datos(anio_publicacion=1499, isbn="123"),
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Libro.objects.count(), 0)

    def test_post_valido_guarda_y_redirige(self):
        resp = self.client.post(
            reverse("libro_create"),
            datos(),
        )

        self.assertRedirects(
            resp,
            reverse("libro_list"),
        )
        self.assertEqual(Libro.objects.count(), 1)


class AutenticacionAutorizacionTests(TestCase):

    def setUp(self):
        self.libro = Libro.objects.create(**datos())

    def test_anonimo_no_puede_ver_listado(self):
        respuesta = self.client.get(reverse("libro_list"))

        self.assertRedirects(
            respuesta,
            "/login/?next=/",
        )

    def test_anonimo_no_puede_crear(self):
        respuesta = self.client.post(
            reverse("libro_create"),
            datos(isbn="0306406152"),
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Libro.objects.count(), 1)

    def test_anonimo_no_puede_editar(self):
        respuesta = self.client.post(
            reverse("libro_update", args=[self.libro.pk]),
            datos(titulo="Título modificado"),
        )

        self.assertEqual(respuesta.status_code, 302)
        self.libro.refresh_from_db()
        self.assertEqual(
            self.libro.titulo,
            "Cien años de soledad",
        )

    def test_anonimo_no_puede_eliminar(self):
        respuesta = self.client.post(
            reverse("libro_delete", args=[self.libro.pk]),
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(
            Libro.objects.filter(pk=self.libro.pk).exists()
        )

    def test_usuario_sin_permisos_recibe_403(self):
        usuario = crear_usuario("sin_permisos")
        self.client.force_login(usuario)

        for nombre in ("libro_list", "libro_create"):
            with self.subTest(ruta=nombre):
                respuesta = self.client.get(reverse(nombre))
                self.assertEqual(respuesta.status_code, 403)

    def test_lector_puede_consultar_pero_no_crear(self):
        usuario = crear_usuario(
            "lector",
            permisos=("view_libro",),
        )
        self.client.force_login(usuario)

        self.assertEqual(
            self.client.get(reverse("libro_list")).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(
                reverse("libro_create"),
                datos(isbn="0306406152"),
            ).status_code,
            403,
        )
        self.assertEqual(Libro.objects.count(), 1)

    def test_usuario_sin_permiso_no_puede_editar(self):
        usuario = crear_usuario(
            "lector_edicion",
            permisos=("view_libro",),
        )
        self.client.force_login(usuario)

        respuesta = self.client.post(
            reverse("libro_update", args=[self.libro.pk]),
            datos(titulo="Cambio prohibido"),
        )

        self.assertEqual(respuesta.status_code, 403)
        self.libro.refresh_from_db()
        self.assertEqual(
            self.libro.titulo,
            "Cien años de soledad",
        )

    def test_usuario_sin_permiso_no_puede_eliminar(self):
        usuario = crear_usuario(
            "lector_eliminacion",
            permisos=("view_libro",),
        )
        self.client.force_login(usuario)

        respuesta = self.client.post(
            reverse("libro_delete", args=[self.libro.pk]),
        )

        self.assertEqual(respuesta.status_code, 403)
        self.assertTrue(
            Libro.objects.filter(pk=self.libro.pk).exists()
        )


class LoginLogoutTests(TestCase):

    def setUp(self):
        self.usuario = crear_usuario("usuario_login")
        self.clave = "ClaveTemporal-Pruebas-2026!"

    def test_login_correcto(self):
        respuesta = self.client.post(
            reverse("login"),
            {
                "username": "usuario_login",
                "password": self.clave,
            },
        )

        self.assertRedirects(
            respuesta,
            reverse("libro_list"),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            self.usuario.pk,
        )

    def test_login_incorrecto(self):
        respuesta = self.client.post(
            reverse("login"),
            {
                "username": "usuario_login",
                "password": "incorrecta",
            },
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )
        self.assertContains(
            respuesta,
            "Usuario o contraseña incorrectos",
        )

    def test_logout_rechaza_get_y_acepta_post(self):
        self.client.force_login(self.usuario)

        respuesta_get = self.client.get(reverse("logout"))
        self.assertEqual(respuesta_get.status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)

        respuesta_post = self.client.post(reverse("logout"))

        self.assertRedirects(
            respuesta_post,
            reverse("login"),
        )
        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_logout_requiere_csrf(self):
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.usuario)

        respuesta = cliente.post(reverse("logout"))

        self.assertEqual(respuesta.status_code, 403)
        self.assertIn(
            "_auth_user_id",
            cliente.session,
        )
