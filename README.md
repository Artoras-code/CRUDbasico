# 📚 CRUDbasico — Biblioteca Segura

Aplicación web de gestión de libros desarrollada con **Python y Django**, como parte de la **Evaluación 3 de Desarrollo Seguro**.

El proyecto implementa operaciones CRUD, autenticación de usuarios, control de permisos y distintas medidas de seguridad. Se ejecuta mediante Docker Compose y utiliza Gunicorn como servidor WSGI.

## Funcionalidades

- Inicio y cierre de sesión.
- Listado de libros para usuarios autenticados.
- Creación, edición y eliminación de libros según permisos.
- Validación de formularios y datos.
- Interfaz web con estilos CSS externos.
- Persistencia de datos mediante SQLite.

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Django | Framework web |
| SQLite | Base de datos |
| Docker y Docker Compose | Contenedorización |
| Gunicorn | Servidor WSGI |
| WhiteNoise | Archivos estáticos |
| OWASP ZAP | Análisis dinámico de seguridad |
| SonarQube | Análisis estático de código |
| Coverage.py | Cobertura de pruebas |
| Git y GitHub | Control de versiones |

## Instalación y ejecución con Docker

### 1. Clonar el repositorio

```bash
git clone -b evaluacion-3-seguridad https://github.com/Artoras-code/CRUDbasico.git
cd CRUDbasico
```

### 2. Configurar las variables de entorno

Crear un archivo `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

Generar una clave secreta para Django:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Guardar el valor generado en `DJANGO_SECRET_KEY` dentro de `.env`.

Configurar también:

```dotenv
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

No publicar el archivo `.env` en GitHub.

### 3. Construir e iniciar los contenedores

```bash
sudo docker compose up -d --build
```

### 4. Ejecutar las migraciones

```bash
sudo docker compose exec web python manage.py migrate
```

### 5. Crear un usuario administrador

```bash
sudo docker compose exec web python manage.py createsuperuser
```

### 6. Abrir la aplicación

Acceder desde el navegador:

http://127.0.0.1:8000/login/

La aplicación utiliza un volumen Docker para conservar los datos de SQLite entre recreaciones del contenedor.

## Medidas de seguridad implementadas

- Autenticación obligatoria para acceder al catálogo.
- Autorización basada en permisos de Django.
- Restricción de métodos HTTP en las vistas.
- Protección CSRF mediante Django.
- Gestión de `SECRET_KEY` mediante variables de entorno.
- `DEBUG` desactivado en el contenedor.
- Cabeceras de seguridad HTTP y política Content Security Policy (CSP).
- Restricciones de CORS.
- CSS externo compatible con la política CSP.
- Cookies de sesión configuradas con atributos de seguridad.
- Servidor Gunicorn sin exposición explícita de versiones.
- Contenedor ejecutado mediante un usuario sin privilegios de root.
- Puerto publicado únicamente en `127.0.0.1`.

## Pruebas automatizadas

Se implementaron **22 pruebas automatizadas de Django**, todas aprobadas en la verificación final.

Para ejecutarlas en un entorno Python configurado:

```bash
python manage.py collectstatic --noinput
python manage.py test
```

Para medir cobertura con Coverage.py:

```bash
python -m coverage run --source=libros,config manage.py test
python -m coverage report -m
python -m coverage xml -o coverage.xml
```

Resultados obtenidos:

- 22 pruebas aprobadas.
- 0 errores en la ejecución final.
- 91 % de cobertura reportada por Coverage.py.

## Análisis de seguridad

### OWASP ZAP

Se utilizó OWASP ZAP para comparar una línea base reconstruida de la aplicación con su versión corregida.

Las correcciones incluyeron la incorporación de CSP, restricciones CORS y la sustitución del servidor de desarrollo por Gunicorn.

En las páginas y recursos analizados de la versión corregida dejaron de detectarse los hallazgos originales de ausencia de CSP y exposición de versiones del servidor.

### SonarQube

Se ejecutó un análisis estático sobre el proyecto `CRUDbasico`.

| Métrica | Resultado final |
|---|---|
| Quality Gate | Passed |
| Problemas de seguridad abiertos | 0 |
| Problemas abiertos totales | 0 |
| Cobertura general | 83,5 % |
| Cobertura de código nuevo | 91,5 % |
| Duplicación | 0 % |
| Líneas de código analizadas | 678 |

El análisis inicial registraba dos problemas de seguridad: una clave secreta de Django incluida en el código y una vista sin métodos HTTP explícitos.

En el análisis posterior ambos hallazgos dejaron de aparecer.

Los resultados corresponden al alcance de las herramientas utilizadas y no constituyen una garantía de ausencia de vulnerabilidades.

## Análisis estático con SonarScanner

Con SonarQube funcionando en `http://localhost:9000`, configurar un token de análisis como variable de entorno `SONAR_TOKEN`.

Ejecutar:

```bash
sonar-scanner -Dsonar.scanner.skipJreProvisioning=true
```

La opción `skipJreProvisioning` permite utilizar el entorno Java local, que debe ser compatible con SonarScanner.

## Control de versiones

El desarrollo de seguridad se encuentra en la rama:

`evaluacion-3-seguridad`

Los cambios se registraron mediante commits separados para autenticación, permisos, endurecimiento de seguridad, Docker, CSP, Gunicorn y SonarQube.

## Alcance

Este proyecto está configurado como laboratorio académico local. El uso de SQLite, el servidor expuesto en loopback y la configuración de pruebas no sustituyen una arquitectura de producción.

---

**Proyecto académico — Evaluación 3 de Desarrollo Seguro.**