from rest_framework.routers import DefaultRouter
from apps.sepomex.api.viewsets import (
    EstadoViewSet, MunicipioViewSet, AsentamientoViewSet, CargaSepomexViewSet
)

router = DefaultRouter()
router.register("estado",        EstadoViewSet,       basename="estado")
router.register("municipio",     MunicipioViewSet,    basename="municipio")
router.register("asentamiento",  AsentamientoViewSet, basename="asentamiento")
router.register("carga",         CargaSepomexViewSet, basename="carga-sepomex")

sepomex_urls = router.urls
