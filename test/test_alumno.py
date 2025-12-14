#nuevo test alumno con mapping integrado.
import unittest
import os
from flask import current_app
from app import create_app, db
from app.models.alumno import Alumno
from app.services.alumno_service import AlumnoService
from app.mapping.alumno_mapping import AlumnoSchema

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Configuración previa a cada test"""
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Limpieza posterior a cada test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_alumno_creation(self):
        """Prueba la instanciación del objeto Alumno en memoria"""
        alumno = self.__nuevo_alumno()
        self.assertIsNotNone(alumno)
        self.assertEqual(alumno.apellido, "Silva")
        self.assertEqual(alumno.nombre, "Abril")
        self.assertEqual(alumno.nro_documento, "12345678")
        self.assertEqual(alumno.sexo, "F")
        self.assertEqual(alumno.nro_legajo, 1234)
        

    def test_alumno_busqueda(self):
        """Prueba buscar un alumno por su ID"""
        alumno = self.__nuevo_alumno()
        db.session.add(alumno)
        db.session.commit()  
        
        resultado = AlumnoService.buscar_por_id(alumno.id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nro_documento, "12345678")
        self.assertEqual(resultado.nro_legajo, 1234)

    def test_buscar_todos_los_alumnos(self):
        """Prueba recuperar una lista de todos los alumnos"""
        # Creamos dos alumnos con datos DISTINTOS para evitar errores de restricción unique (DNI/Legajo)
        alumno1 = self.__nuevo_alumno(dni="11111111", legajo=1001)
        alumno2 = self.__nuevo_alumno(dni="22222222", legajo=1002)
        
        db.session.add(alumno1)
        db.session.add(alumno2)
        db.session.commit()
        
        lista_alumnos = AlumnoService.buscar_todos()
        
        self.assertIsNotNone(lista_alumnos)
        self.assertEqual(len(lista_alumnos), 2)

    

    def test_serializacion_alumno(self):
        """
        Prueba de Mapping: Verifica que el objeto Alumno se pueda convertir 
        correctamente a un diccionario/JSON.
        """
        alumno = self.__nuevo_alumno()
        
        schema = AlumnoSchema()
        data = schema.dump(alumno)

        self.assertEqual(data["apellido"], "Silva")
        self.assertEqual(data["nombre"], "Abril")
        self.assertEqual(data["nro_documento"], "12345678")
        self.assertEqual(data["nro_legajo"], 1234)



    def __nuevo_alumno(self, dni="12345678", legajo=1234):
        """
        Helper para crear instancias de Alumno.
        Acepta parámetros para DNI y Legajo para permitir crear múltiples alumnos únicos.
        """
        alumno = Alumno()
        
        alumno.apellido = 'Silva'
        alumno.nombre = 'Abril'
        alumno.nro_documento = dni
        alumno.fecha_nacimiento = '1990-01-01'
        alumno.sexo = 'F'
        alumno.nro_legajo = legajo
        alumno.fecha_ingreso = '2022-01-01'
        
        return alumno

if __name__ == '__main__':
    unittest.main()
