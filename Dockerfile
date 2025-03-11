# Etapa 2: Desarrollo con SSH
FROM python:latest AS api_dev

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia las dependencias instaladas desde la etapa de construcción
COPY . .

# Instala las dependencias de la aplicación
RUN  pip install Django mysqlclient pymysql djangorestframework djangorestframework_simplejwt celery redis django-cors-headers

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando de inicio 
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]

#CMD python manage.py runserver 0.0.0.0:8000