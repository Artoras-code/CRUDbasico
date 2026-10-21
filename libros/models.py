from django.db import models


class Libro(models.Model):
    ESTADOS = [
        ("disponible", "Disponible"),
        ("prestado", "Prestado"),
        ("reservado", "Reservado"),
    ]

    titulo = models.CharField(max_length=120)
    anio_publicacion = models.PositiveSmallIntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="disponible")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} ({self.anio_publicacion})"