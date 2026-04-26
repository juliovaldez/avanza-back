import os
import tempfile

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.filters import OrderingFilter

from api.common.base_models import BaseModelViewSet
from api.utils.utils import json_response
from apps.sepomex.models import Estado, Municipio, Asentamiento, CargaSepomex
from apps.sepomex.api.serializers import (
    EstadoSerializer, MunicipioSerializer,
    AsentamientoSerializer, CargaSepomexSerializer,
)


class EstadoViewSet(BaseModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["nombre", "clave"]


class MunicipioViewSet(BaseModelViewSet):
    queryset = Municipio.objects.select_related("estado").all()
    serializer_class = MunicipioSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["nombre"]

    def get_queryset(self):
        qs = self.queryset
        estado_id = self.request.query_params.get("estado_id")
        if estado_id:
            qs = qs.filter(estado_id=estado_id)
        return qs


class AsentamientoViewSet(BaseModelViewSet):
    queryset = Asentamiento.objects.select_related("municipio__estado").all()
    serializer_class = AsentamientoSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["codigo_postal", "nombre"]

    def get_queryset(self):
        qs = self.queryset
        cp      = self.request.query_params.get("cp")
        estado  = self.request.query_params.get("estado_id")
        mun     = self.request.query_params.get("municipio_id")
        search  = self.request.query_params.get("search")

        if cp:
            qs = qs.filter(codigo_postal__startswith=cp)
        if estado:
            qs = qs.filter(municipio__estado_id=estado)
        if mun:
            qs = qs.filter(municipio_id=mun)
        if search:
            qs = qs.filter(
                Q(nombre__icontains=search) |
                Q(codigo_postal__startswith=search)
            )
        return qs


class CargaSepomexViewSet(BaseModelViewSet):
    queryset = CargaSepomex.objects.all()
    serializer_class = CargaSepomexSerializer
    parser_classes = [MultiPartParser]
    filter_backends = [OrderingFilter]

    @action(detail=False, methods=["post"], url_path="cargar")
    def cargar(self, request):
        archivo = request.FILES.get("archivo")
        if not archivo:
            return json_response(message="No se recibió ningún archivo.", status_code=400)

        # Guardar archivo temporal
        suffix = os.path.splitext(archivo.name)[1]
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        for chunk in archivo.chunks():
            tmp.write(chunk)
        tmp.close()

        carga = CargaSepomex.objects.create(nombre_archivo=archivo.name)

        from apps.sepomex.tasks import procesar_xml_sepomex
        procesar_xml_sepomex.delay(carga.id, tmp.name)

        return json_response(
            data=CargaSepomexSerializer(carga).data,
            message="Archivo recibido. Procesamiento iniciado.",
        )

    @action(detail=False, methods=["get"], url_path="ultimo-estado")
    def ultimo_estado(self, request):
        carga = CargaSepomex.objects.first()
        if not carga:
            return json_response(data=None)
        return json_response(data=CargaSepomexSerializer(carga).data)
