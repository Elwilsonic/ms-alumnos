import unittest
import os
from app import create_app
from app.services.alumno_service import AlumnoService
from test.instancias import nuevoalumno
from app import db

class AlumnoTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_buscar_paginado(self):
        nuevoalumno()
        nuevoalumno()
        alumnos = AlumnoService.buscar_paginado(limit=2, offset=0)
        self.assertIsNotNone(alumnos)
        self.assertEqual(len(alumnos), 2)

    def test_buscar_por_id(self):
        alumno = nuevoalumno(nombre="Ana", apellido="García", nrodocumento="12345678")
        encontrado = AlumnoService.buscar_por_id(alumno.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "Ana")
        self.assertEqual(encontrado.apellido, "García")