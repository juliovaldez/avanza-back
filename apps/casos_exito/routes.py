from rest_framework.routers import DefaultRouter
from apps.casos_exito.api.viewsets import CasoExitoViewSet

router = DefaultRouter()
router.register("", CasoExitoViewSet)

caso_exito_urls = router.urls
