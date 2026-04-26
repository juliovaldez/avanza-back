import os
from xml.etree.ElementTree import iterparse
from celery import shared_task
from django.db import transaction


@shared_task(bind=True)
def procesar_xml_sepomex(self, carga_id: int, file_path: str):
    from apps.sepomex.models import Estado, Municipio, Asentamiento, CargaSepomex

    carga = CargaSepomex.objects.get(id=carga_id)
    carga.estado_proceso = CargaSepomex.Estado.PROCESANDO
    carga.save(update_fields=["estado_proceso"])

    try:
        estados_map = {}    # clave -> nombre
        municipios_map = {} # (c_estado, c_mnpio) -> nombre
        rows = []

        # Streaming parse — no carga todo el XML en memoria
        for event, elem in iterparse(file_path, events=["end"]):
            tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag != "table":
                continue

            get = lambda f: (elem.find(f"{{{elem.tag.split('{')[1].split('}')[0]}}}{f}") if "{" in elem.tag else elem.find(f)).text or "" if (elem.find(f"{{{elem.tag.split('{')[1].split('}')[0]}}}{f}") if "{" in elem.tag else elem.find(f)) is not None else ""

            # Helper namespace-aware
            ns = elem.tag.split("}")[0].lstrip("{") if "}" in elem.tag else ""
            def fv(name):
                e = elem.find(f"{{{ns}}}{name}") if ns else elem.find(name)
                return e.text.strip() if e is not None and e.text else ""

            c_estado = fv("c_estado")
            d_estado = fv("d_estado")
            c_mnpio  = fv("c_mnpio")
            d_mnpio  = fv("D_mnpio")

            if c_estado:
                estados_map[c_estado] = d_estado
            if c_estado and c_mnpio:
                municipios_map[(c_estado, c_mnpio)] = d_mnpio

            rows.append({
                "codigo_postal": fv("d_codigo"),
                "nombre":        fv("d_asenta"),
                "tipo":          fv("d_tipo_asenta"),
                "zona":          fv("d_zona"),
                "ciudad":        fv("d_ciudad"),
                "c_estado":      c_estado,
                "c_mnpio":       c_mnpio,
            })
            elem.clear()

        carga.total_registros = len(rows)
        carga.save(update_fields=["total_registros"])

        with transaction.atomic():
            # Limpiar datos anteriores
            Asentamiento.objects.all().delete()
            Municipio.objects.all().delete()
            Estado.objects.all().delete()

            # Insertar Estados
            estado_objs = {
                clave: Estado(clave=clave, nombre=nombre)
                for clave, nombre in estados_map.items()
            }
            Estado.objects.bulk_create(list(estado_objs.values()))
            # Recargar IDs
            estado_db = {e.clave: e for e in Estado.objects.all()}

            # Insertar Municipios
            municipio_objs = {}
            mun_bulk = []
            for (c_est, c_mun), nombre in municipios_map.items():
                if c_est in estado_db:
                    key = (c_est, c_mun)
                    obj = Municipio(clave=c_mun, nombre=nombre, estado=estado_db[c_est])
                    municipio_objs[key] = obj
                    mun_bulk.append(obj)
            Municipio.objects.bulk_create(mun_bulk)
            # Recargar IDs
            municipio_db = {(m.clave, m.estado.clave): m for m in Municipio.objects.select_related("estado").all()}

            # Insertar Asentamientos en lotes
            BATCH = 3000
            total = len(rows)
            procesados = 0
            batch = []
            for row in rows:
                key = (row["c_mnpio"], row["c_estado"])
                mun = municipio_db.get(key)
                if mun:
                    batch.append(Asentamiento(
                        codigo_postal=row["codigo_postal"],
                        nombre=row["nombre"],
                        tipo=row["tipo"],
                        zona=row["zona"],
                        ciudad=row["ciudad"],
                        municipio=mun,
                    ))
                if len(batch) >= BATCH:
                    Asentamiento.objects.bulk_create(batch)
                    procesados += len(batch)
                    batch = []
                    carga.registros_procesados = procesados
                    carga.save(update_fields=["registros_procesados"])

            if batch:
                Asentamiento.objects.bulk_create(batch)
                procesados += len(batch)

        carga.registros_procesados = procesados
        carga.estado_proceso = CargaSepomex.Estado.COMPLETADO
        carga.mensaje = f"Importados {procesados:,} asentamientos, {len(estado_db)} estados, {len(municipio_db)} municipios."
        carga.save(update_fields=["registros_procesados", "estado_proceso", "mensaje"])

    except Exception as exc:
        carga.estado_proceso = CargaSepomex.Estado.ERROR
        carga.mensaje = str(exc)
        carga.save(update_fields=["estado_proceso", "mensaje"])
        raise

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
