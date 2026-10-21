import re
from datetime import date

from django import forms

from .models import Libro

ANIO_MIN = 1500
TITULO_MIN = 3
TITULO_MAX = 120


class LibroForm(forms.ModelForm):
    """Validación del servidor para crear y editar libros.

    Las restricciones HTML (min, max, maxlength) son solo ayuda visual;
    las reglas reales se aplican en los métodos clean_*.
    """

    isbn = forms.CharField(
        label="ISBN",
        max_length=17,  # 13 dígitos + hasta 4 separadores; se normaliza en clean_isbn
        help_text="10 o 13 dígitos. Se permiten guiones o espacios.",
    )

    class Meta:
        model = Libro
        fields = ["titulo", "anio_publicacion", "isbn", "estado"]
        labels = {
            "titulo": "Título",
            "anio_publicacion": "Año de publicación",
            "estado": "Estado",
        }

    def clean_titulo(self):
        titulo = " ".join(self.cleaned_data["titulo"].split())
        if not (TITULO_MIN <= len(titulo) <= TITULO_MAX):
            raise forms.ValidationError(
                f"El título debe tener entre {TITULO_MIN} y {TITULO_MAX} caracteres."
            )
        return titulo

    def clean_anio_publicacion(self):
        anio = self.cleaned_data["anio_publicacion"]
        anio_max = date.today().year
        if not (ANIO_MIN <= anio <= anio_max):
            raise forms.ValidationError(
                f"El año debe estar entre {ANIO_MIN} y {anio_max}."
            )
        return anio

    def clean_isbn(self):
        # Se aceptan guiones o espacios como separadores; se guarda solo dígitos.
        isbn = re.sub(r"[\s-]", "", self.cleaned_data["isbn"])
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise forms.ValidationError(
                "El ISBN debe tener 10 o 13 dígitos (se permiten guiones)."
            )
        return isbn