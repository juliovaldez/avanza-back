# admin_api/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# Establece el módulo de configuración de Django para que Celery lo use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_api.settings')

app = Celery('admin_api')

# Carga las configuraciones de Celery desde las settings de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre y carga tareas definidas en aplicaciones registradas en Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

    
    
