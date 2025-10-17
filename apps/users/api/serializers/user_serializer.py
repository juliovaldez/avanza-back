from rest_framework import serializers
from django.contrib.auth.models import Group
from apps.users.models import User
from api.common.base_models import BaseModelSerializer

class UserSerializer(BaseModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(),required=False)
    
    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = ["id","username", "email", "first_name", "last_name", "groups"]



class UserProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "last_name", "is_superuser", "groups", "permissions"]

    def get_groups(self, user_instance: User):
        return user_instance.groups.values_list("name", flat=True)

    def get_permissions(self, user_instance: User):
        return list(user_instance.get_all_permissions())
