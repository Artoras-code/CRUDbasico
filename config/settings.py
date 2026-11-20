
import os
from pathlib import Path

from dotenv import load_dotenv


# =====================================================
# RUTAS DEL PROYECTO
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga .env sin sobrescribir variables del sistema.
load_dotenv(BASE_DIR / ".env")


# =====================================================
# CONFIGURACIÓN DE SEGURIDAD
# =====================================================

DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

# La clave secreta debe venir del entorno.
# Nunca utilizar una clave fija en el repositorio.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "Falta la variable de entorno DJANGO_SECRET_KEY."
    )

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]


# =====================================================
# APLICACIONES INSTALADAS
# =====================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Aplicación del CRUD
    "libros",
]


# =====================================================
# MIDDLEWARE
# =====================================================


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "config.security_middleware.ContentSecurityPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =====================================================
# URLS Y PLANTILLAS
# =====================================================

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"



# =====================================================
# BASE DE DATOS
# =====================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get(
            "DJANGO_DB_PATH",
            str(BASE_DIR / "db.sqlite3"),
        ),
    }
}

# =====================================================
# VALIDACIÓN DE CONTRASEÑAS
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =====================================================
# INTERNACIONALIZACIÓN
# =====================================================

LANGUAGE_CODE = "es-cl"

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_TZ = True


# =====================================================
# ARCHIVOS ESTÁTICOS
# =====================================================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# =====================================================
# CLAVE PRIMARIA POR DEFECTO
# =====================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =====================================================
# AUTENTICACIÓN Y REDIRECCIONES
# =====================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "libro_list"

LOGOUT_REDIRECT_URL = "login"


# =====================================================
# SEGURIDAD DE COOKIES Y SESIONES
# =====================================================

# Impide que JavaScript acceda a las cookies.
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Mitiga ciertos ataques CSRF entre sitios.
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# Duración de sesión: 30 minutos.
SESSION_COOKIE_AGE = 1800

# La sesión expira al cerrar el navegador.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Cookies Secure cuando la aplicación utiliza HTTPS.
# En desarrollo HTTP local permanecen desactivadas.
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Impide que la aplicación sea embebida en iframes.
X_FRAME_OPTIONS = "DENY"

# Evita que el navegador interprete incorrectamente
# tipos MIME declarados por el servidor.
SECURE_CONTENT_TYPE_NOSNIFF = True

# HTTPS debe activarse solamente cuando el entorno
# esté correctamente configurado para utilizar TLS.
SECURE_SSL_REDIRECT = (
    os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "0") == "1"
)

# HSTS se configura cuando exista HTTPS real.
SECURE_HSTS_SECONDS = 0


WHITENOISE_ALLOW_ALL_ORIGINS = False