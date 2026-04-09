# Etapa 2: Desarrollo con SSH
FROM  python:3.14 AS avanza_api_dev

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia las dependencias instaladas desde la etapa de construcción
COPY . .

# Instala las dependencias de la aplicación
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r req.txt

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando de inicio 
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]

#CMD python manage.py runserver 0.0.0.0:8000





FROM python:3.14  AS avanza_api_prod

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r req.txt


# Ejecuta collectstatic
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Ejecuta gunicorn con whitenoise (sirve estáticos desde /static/)
CMD ["gunicorn", "avanza_api.wsgi:application", "--bind", "0.0.0.0:8000"]