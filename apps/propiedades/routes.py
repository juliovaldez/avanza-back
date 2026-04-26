from rest_framework.routers import DefaultRouter
from apps.propiedades.api.viewsets import PropiedadViewSet

router = DefaultRouter()
router.register("propiedad", PropiedadViewSet, basename="propiedad")

propiedades_urls = router.urls
