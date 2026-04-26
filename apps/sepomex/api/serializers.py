from rest_framework import serializers
from apps.sepomex.models import Estado, Municipio, Asentamiento, CargaSepomex


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ["id", "clave", "nombre"]


class MunicipioSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = Municipio
        fields = ["id", "clave", "nombre", "estado_id", "estado_nombre"]


class AsentamientoSerializer(serializers.ModelSerializer):
    municipio_nombre = serializers.CharField(source="municipio.nombre",        read_only=True)
    estado_id        = serializers.IntegerField(source="municipio.estado_id",  read_only=True)
    estado_nombre    = serializers.CharField(source="municipio.estado.nombre", read_only=True)
    estado_clave     = serializers.CharField(source="municipio.estado.clave",  read_only=True)

    class Meta:
        model = Asentamiento
        fields = [
            "id", "codigo_postal", "nombre", "tipo", "zona", "ciudad",
            "municipio_id", "municipio_nombre",
            "estado_id", "estado_nombre", "estado_clave",
        ]


class CargaSepomexSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaSepomex
        fields = [
            "id", "nombre_archivo", "fecha_carga", "estado_proceso",
            "total_registros", "registros_procesados", "mensaje",
        ]
