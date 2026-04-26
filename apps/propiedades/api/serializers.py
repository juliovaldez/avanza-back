from rest_framework import serializers
from api.common.base_models import BaseModelSerializer
from apps.propiedades.models import Propiedad
from apps.catalogs.models import Equipamiento


class PropiedadSerializer(BaseModelSerializer):
    # Campos de lectura para mostrar el nombre de cada FK
    tipo_propiedad_nombre       = serializers.CharField(source="tipo_propiedad.nombre",       read_only=True, default=None, allow_null=True)
    calidad_construccion_nombre = serializers.CharField(source="calidad_construccion.nombre", read_only=True, default=None, allow_null=True)
    estado_conservacion_nombre  = serializers.CharField(source="estado_conservacion.nombre",  read_only=True, default=None, allow_null=True)
    tipo_acabado_nombre         = serializers.CharField(source="tipo_acabado.nombre",         read_only=True, default=None, allow_null=True)
    documento_propiedad_nombre  = serializers.CharField(source="documento_propiedad.nombre",  read_only=True, default=None, allow_null=True)
    predial_nombre              = serializers.CharField(source="predial.nombre",              read_only=True, default=None, allow_null=True)
    servicios_corriente_nombre  = serializers.CharField(source="servicios_corriente.nombre",  read_only=True, default=None, allow_null=True)
    gravamen_nombre             = serializers.CharField(source="gravamen.nombre",             read_only=True, default=None, allow_null=True)
    situacion_legal_nombre      = serializers.CharField(source="situacion_legal.nombre",      read_only=True, default=None, allow_null=True)

    # Ubicación (read-only, derivados de asentamiento)
    asentamiento_cp           = serializers.CharField(source="asentamiento.codigo_postal",           read_only=True, default=None, allow_null=True)
    asentamiento_colonia      = serializers.CharField(source="asentamiento.nombre",                  read_only=True, default=None, allow_null=True)
    asentamiento_ciudad       = serializers.CharField(source="asentamiento.ciudad",                  read_only=True, default=None, allow_null=True)
    asentamiento_municipio_id = serializers.IntegerField(source="asentamiento.municipio_id",         read_only=True, default=None, allow_null=True)
    asentamiento_municipio    = serializers.CharField(source="asentamiento.municipio.nombre",        read_only=True, default=None, allow_null=True)
    asentamiento_estado_id    = serializers.IntegerField(source="asentamiento.municipio.estado_id",  read_only=True, default=None, allow_null=True)
    asentamiento_estado       = serializers.CharField(source="asentamiento.municipio.estado.nombre", read_only=True, default=None, allow_null=True)

    # M2M: acepta y devuelve lista de IDs; DRF gestiona set() automáticamente
    equipamiento = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Equipamiento.objects.all(),
        required=False,
    )
    equipamiento_nombres = serializers.SerializerMethodField(read_only=True)

    def get_equipamiento_nombres(self, obj):
        return list(obj.equipamiento.values_list("nombre", flat=True))

    class Meta(BaseModelSerializer.Meta):
        model  = Propiedad
        fields = [
            "id",
            # General
            "tipo_propiedad", "tipo_propiedad_nombre",
            "metros_terreno", "metros_construccion", "precio",
            # Características
            "habitaciones", "banos", "medio_bano",
            "niveles", "cochera", "antiguedad",
            # Calidad
            "calidad_construccion", "calidad_construccion_nombre",
            "estado_conservacion",  "estado_conservacion_nombre",
            "tipo_acabado",         "tipo_acabado_nombre",
            "mantenimiento",
            "equipamiento",         "equipamiento_nombres",
            # Documentación
            "documento_propiedad",  "documento_propiedad_nombre",
            "predial",              "predial_nombre",
            "servicios_corriente",  "servicios_corriente_nombre",
            "gravamen",             "gravamen_nombre",
            "situacion_legal",      "situacion_legal_nombre",
            # Ubicación
            "asentamiento",
            "asentamiento_cp", "asentamiento_colonia", "asentamiento_ciudad",
            "asentamiento_municipio_id", "asentamiento_municipio",
            "asentamiento_estado_id", "asentamiento_estado",
        ]
