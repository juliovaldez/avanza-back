from api.utils.utils import json_response
from rest_framework import viewsets

class BaseMixin(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return json_response(data=response.status_code,message='Recurso creado correctamente')

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return json_response(data=response.data,message='Recurso actualizado correctamente' )

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return json_response(data=response.data,message='Recurso eliminado correctamente')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return json_response(data=response.data, paginate=True)
        
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return json_response(data=response.data)