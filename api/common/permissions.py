
from rest_framework import permissions

class DjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        super().__init__()
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]
        

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            pass
        else:
            access_token = getattr(request, 'auth', None)
            if access_token and hasattr(access_token, 'application') and access_token.application.user:
                user = access_token.application.user
            else:
                return False
            
        model_cls = getattr(view.queryset, 'model', None)
        if not model_cls:
            return False
        
        perms = self.get_required_permissions(request.method, model_cls)
        has_perm = user.has_perms(perms)
        return has_perm