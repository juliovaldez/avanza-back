from rest_framework.routers import DefaultRouter
from apps.users.api.viewsets.user_viewset import UserViewSet
from apps.users.api.viewsets.auth_viewsets import AuthViewSet
from apps.users.api.viewsets.permission_viewsets import PermissionViewSet
from apps.users.api.viewsets.group_viewsets import GroupViewSet

router = DefaultRouter()
router.register('', UserViewSet)
user_urls = router.urls

router = DefaultRouter()
router.register('', AuthViewSet,basename='auth')
auth_urls = router.urls

router = DefaultRouter()
router.register("", GroupViewSet)
groups_urls = router.urls

router = DefaultRouter()
router.register("", PermissionViewSet)
permissions_urls = router.urls



