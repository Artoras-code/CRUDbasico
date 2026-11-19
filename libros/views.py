
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import LibroForm
from .models import Libro


# =====================================================
# LISTAR LIBROS
# Requiere autenticación y permiso de consulta.
# =====================================================

@login_required
@permission_required("libros.view_libro", raise_exception=True)
@require_GET
def libro_list(request):
    libros = Libro.objects.all()

    return render(
        request,
        "libros/libro_list.html",
        {"libros": libros},
    )


# =====================================================
# CREAR LIBRO
# Requiere autenticación y permiso de creación.
# =====================================================

@login_required
@permission_required("libros.add_libro", raise_exception=True)
@require_http_methods(["GET", "POST"])
def libro_create(request):
    if request.method == "POST":
        form = LibroForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Libro creado correctamente.",
            )

            return redirect("libro_list")
    else:
        form = LibroForm()

    return render(
        request,
        "libros/libro_form.html",
        {
            "form": form,
            "accion": "Crear",
        },
    )


# =====================================================
# EDITAR LIBRO
# Requiere autenticación y permiso de modificación.
# =====================================================

@login_required
@permission_required("libros.change_libro", raise_exception=True)
@require_http_methods(["GET", "POST"])
def libro_update(request, pk):
    libro = get_object_or_404(Libro, pk=pk)

    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Libro actualizado correctamente.",
            )

            return redirect("libro_list")
    else:
        form = LibroForm(instance=libro)

    return render(
        request,
        "libros/libro_form.html",
        {
            "form": form,
            "accion": "Editar",
        },
    )


# =====================================================
# ELIMINAR LIBRO
# Requiere autenticación y permiso de eliminación.
# =====================================================

@login_required
@permission_required("libros.delete_libro", raise_exception=True)
@require_http_methods(["GET", "POST"])
def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)

    if request.method == "POST":
        libro.delete()

        messages.success(
            request,
            "Libro eliminado correctamente.",
        )

        return redirect("libro_list")

    return render(
        request,
        "libros/libro_confirm_delete.html",
        {"libro": libro},
    )
