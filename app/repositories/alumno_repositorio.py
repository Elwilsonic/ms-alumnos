from app import db
from app.models import Alumno

class AlumnoRepository:
    @staticmethod
    def buscar_paginado(limit: int = 100, offset: int = 0):
        return db.session.query(Alumno).limit(limit).offset(offset).all()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Alumno).filter_by(id=id).first()