from flask import jsonify, Blueprint, request
from app.mapping.alumno_mapping import AlumnoMapping
from app.services.alumno_service import AlumnoService

alumno_bp = Blueprint('alumno', __name__)
alumno_mapping = AlumnoMapping()

@alumno_bp.route('/alumno', methods=['GET'])
def buscar_todos():
    limit = request.args.get('limit', default=100, type=int)
    offset = request.args.get('offset', default=0, type=int)
    alumnos = AlumnoService.buscar_paginado(limit=limit, offset=offset)
    return alumno_mapping.dump(alumnos, many=True), 200