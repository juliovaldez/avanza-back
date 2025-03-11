from rest_framework import viewsets
from django.contrib.auth.models import Permission
from apps.users.api.serializers.permission_serializers import PermissionSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from api.utils.utils import json_response

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return json_response(data=response.data, paginate=True)
        
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return json_response(data=response.data)
