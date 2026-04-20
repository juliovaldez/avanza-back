from rest_framework.routers import DefaultRouter
from apps.contacto.api.viewsets import ContactoConfigViewSet

router = DefaultRouter()
router.register("", ContactoConfigViewSet)

contacto_urls = router.urls
