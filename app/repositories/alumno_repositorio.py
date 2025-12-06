from app import db
from app.models import Alumno

class AlumnoRepository:
    @staticmethod
    def buscar_paginado(limit: int = 100, offset: int = 0):
        return db.session.query(Alumno).limit(limit).offset(offset).all()