from rest_framework import viewsets
from django.contrib.auth.models import Group
from apps.users.api.serializers.group_serializers import GroupSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.request import Request
from api.utils.utils import json_response
from api.common.base_models import BaseModelViewSet

class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    ordering_fields = ['id','name','permissions']
