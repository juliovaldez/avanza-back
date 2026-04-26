from rest_framework.routers import DefaultRouter
from apps.catalogs.api.viewsets import (
    TipoPropiedadViewSet,
    CalidadConstruccionViewSet, EstadoConservacionViewSet,
    TipoAcabadoViewSet, MantenimientoViewSet, EquipamientoViewSet,
    DocumentoPropiedadViewSet, PredialViewSet, ServiciosCorrienteViewSet,
    GravamenViewSet, SituacionLegalViewSet,
)

router = DefaultRouter()
router.register("tipo-propiedad",  TipoPropiedadViewSet,  basename="tipo-propiedad")
router.register("calidad-construccion", CalidadConstruccionViewSet, basename="calidad-construccion")
router.register("estado-conservacion",  EstadoConservacionViewSet,  basename="estado-conservacion")
router.register("tipo-acabado",         TipoAcabadoViewSet,         basename="tipo-acabado")
router.register("mantenimiento",        MantenimientoViewSet,       basename="mantenimiento")
router.register("equipamiento",         EquipamientoViewSet,         basename="equipamiento")
router.register("documento-propiedad",  DocumentoPropiedadViewSet,   basename="documento-propiedad")
router.register("predial",              PredialViewSet,              basename="predial")
router.register("servicios-corriente",  ServiciosCorrienteViewSet,   basename="servicios-corriente")
router.register("gravamen",             GravamenViewSet,             basename="gravamen")
router.register("situacion-legal",      SituacionLegalViewSet,       basename="situacion-legal")

catalogs_urls = router.urls
