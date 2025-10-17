# Etapa 2: Desarrollo con SSH
FROM python:latest AS sphere_api_dev

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia las dependencias instaladas desde la etapa de construcción
COPY . .

# Instala las dependencias de la aplicación
RUN  pip install Django mysqlclient pymysql djangorestframework djangorestframework_simplejwt celery django_celery_beat redis django-cors-headers django-oauth-toolkit whitenoise

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando de inicio 
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]

#CMD python manage.py runserver 0.0.0.0:8000





FROM python:latest AS sphere_api_prod

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Django mysqlclient pymysql djangorestframework djangorestframework_simplejwt celery django_celery_beat redis django-cors-headers django-oauth-toolkit whitenoise gunicorn


# Ejecuta collectstatic
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Ejecuta gunicorn con whitenoise (sirve estáticos desde /static/)
CMD ["gunicorn", "sphere_api.wsgi:application", "--bind", "0.0.0.0:8000"]