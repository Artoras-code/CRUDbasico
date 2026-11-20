
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Crear usuario sin privilegios
RUN groupadd --system appuser && \
    useradd --system --gid appuser --home-dir /app appuser

# Instalar las dependencias de Django y Gunicorn
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto sin secretos
COPY --chown=appuser:appuser . .

# Preparar el almacenamiento persistente de SQLite
RUN mkdir -p /app/data && \
    chown appuser:appuser /app/data

# Recopilar los archivos estáticos durante la construcción
RUN DJANGO_SECRET_KEY="$(python -c \
    'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" \
    DJANGO_DEBUG=0 \
    python manage.py collectstatic --noinput

# Ejecutar Django sin privilegios de root
USER appuser

EXPOSE 8000

# Iniciar Django mediante Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]
