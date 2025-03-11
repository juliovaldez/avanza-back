from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from apps.users.api.serializers.permission_serializers import PermissionSerializer
from api.common.base_models import BaseModelSerializer

class GroupSerializer(BaseModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all()
    )

    class Meta(BaseModelSerializer.Meta):
        model = Group
        fields = "__all__"

    def create(self, validated_data):
        permissions = validated_data.pop("permissions")
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions)
        return group

    def update(self, instance: Group, validated_data):
        permissions = validated_data.pop("permissions")
        instance.name = validated_data.get("name")
        instance.permissions.set(permissions)
        return instance
