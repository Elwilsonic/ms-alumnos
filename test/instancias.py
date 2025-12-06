from app.models import (
    Alumno, TipoDocumento
)
from datetime import date

from app.services import (
    TipoDocumentoService
    
)

def nuevotipodocumento(sigla="DNI", nombre="Documento Nacional de Identidad",):
    tipo_documento = TipoDocumento()
    tipo_documento.sigla = sigla
    tipo_documento.nombre = nombre
    TipoDocumentoService.crear(tipo_documento)
    return tipo_documento


def nuevoalumno(nombre="Juan", apellido="Pérez", nrodocumento="46291002", tipo_documento=None,
                fecha_nacimiento=date(1990, 1, 1), sexo="M", nro_legajo=123456, fecha_ingreso=date(2020, 1, 1),especialidad=None):
    from app import db
    alumno = Alumno()
    alumno.nombre = nombre
    alumno.apellido = apellido
    alumno.nrodocumento = nrodocumento
    alumno.tipo_documento = tipo_documento or nuevotipodocumento()
    alumno.fecha_nacimiento = fecha_nacimiento
    alumno.sexo = sexo
    alumno.nro_legajo = nro_legajo
    alumno.fecha_ingreso = fecha_ingreso
    alumno.especialidad = especialidad 
    db.session.add(alumno)
    db.session.commit()
    return alumno

