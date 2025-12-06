from app.models import Alumno
from app.repositories import AlumnoRepository

class AlumnoService:
    @staticmethod
    def buscar_paginado(limit: int = 100, offset: int = 0) -> list[Alumno]:
        return AlumnoRepository.buscar_paginado(limit=limit, offset=offset)