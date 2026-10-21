from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LibroForm
from .models import Libro


def libro_list(request):
    libros = Libro.objects.all()
    return render(request, "libros/libro_list.html", {"libros": libros})


@require_http_methods(["GET", "POST"])
def libro_create(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Libro creado correctamente.")
            return redirect("libro_list")
    else:
        form = LibroForm()
    return render(request, "libros/libro_form.html", {"form": form, "accion": "Crear"})


@require_http_methods(["GET", "POST"])
def libro_update(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, "Libro actualizado correctamente.")
            return redirect("libro_list")
    else:
        form = LibroForm(instance=libro)
    return render(request, "libros/libro_form.html", {"form": form, "accion": "Editar"})


@require_http_methods(["GET", "POST"])
def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        libro.delete()
        messages.success(request, "Libro eliminado.")
        return redirect("libro_list")
    return render(request, "libros/libro_confirm_delete.html", {"libro": libro})