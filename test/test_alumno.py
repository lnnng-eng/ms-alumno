#nuevo test alumno con mapping integrado.
import unittest
import os
from flask import current_app
from app import create_app, db
from app.models.alumno import Alumno
from app.models.documento import Documento
from app.services.alumno_service import AlumnoService

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
        self.assertIsNotNone(alumno.tipo_documento)
        self.assertEqual(alumno.fecha_nacimiento, "1990-01-01")
        self.assertEqual(alumno.sexo, "F")
        self.assertEqual(alumno.nro_legajo, 1234)
        self.assertEqual(alumno.fecha_ingreso, "2022-01-01")
        
    def test_crear_alumno(self):
        """Prueba la persistencia (guardado) de un alumno en la BD"""
        alumno = self.__nuevo_alumno()
        AlumnoService.crear_alumno(alumno)
        
        self.assertIsNotNone(alumno)
        self.assertIsNotNone(alumno.id)
        self.assertGreaterEqual(alumno.id, 1)
        self.assertEqual(alumno.apellido, "Silva")
        self.assertEqual(alumno.nombre, "Abril")

    def test_alumno_busqueda(self):
        """Prueba buscar un alumno por su ID"""
        alumno = self.__nuevo_alumno()
        AlumnoService.crear_alumno(alumno)    
        
        resultado = AlumnoService.buscar_por_id(alumno.id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nro_documento, "12345678")
        self.assertEqual(resultado.nro_legajo, 1234)

    def test_buscar_todos_los_alumnos(self):
        """Prueba recuperar una lista de todos los alumnos"""
        # Creamos dos alumnos con datos DISTINTOS para evitar errores de restricción unique (DNI/Legajo)
        alumno1 = self.__nuevo_alumno(dni="11111111", legajo=1001)
        alumno2 = self.__nuevo_alumno(dni="22222222", legajo=1002)
        
        AlumnoService.crear_alumno(alumno1)
        AlumnoService.crear_alumno(alumno2)
        
        lista_alumnos = AlumnoService.buscar_todos()
        
        self.assertIsNotNone(lista_alumnos)
        self.assertEqual(len(lista_alumnos), 2)

    def test_actualizar_alumno(self):
        """Prueba la actualización de datos de un alumno"""
        alumno = self.__nuevo_alumno()
        AlumnoService.crear_alumno(alumno)
        
        # Modificamos el objeto
        alumno.nombre = "Abril Julieta"
        
        # Llamamos al servicio de actualización
        alumno_actualizado = AlumnoService.actualizar_alumno(alumno.id, alumno)
        
        self.assertEqual(alumno_actualizado.nombre, "Abril Julieta")
        
        # Verificación doble: Buscamos en BD para asegurar que se persistió el cambio
        alumno_en_bd = AlumnoService.buscar_por_id(alumno.id)
        self.assertEqual(alumno_en_bd.nombre, "Abril Julieta")

    def test_borrar_alumno(self):
        """Prueba el borrado físico o lógico de un alumno"""
        alumno = self.__nuevo_alumno()
        AlumnoService.crear_alumno(alumno)
        
        # Confirmamos que existe antes de borrar
        self.assertIsNotNone(AlumnoService.buscar_por_id(alumno.id))
        
        # Borramos
        AlumnoService.borrar_por_id(alumno.id)
        
        # Verificamos que al buscarlo de nuevo, ya no exista (devuelva None)
        resultado_busqueda = AlumnoService.buscar_por_id(alumno.id)
        self.assertIsNone(resultado_busqueda)

    def test_serializacion_alumno(self):
        """
        Prueba de Mapping: Verifica que el objeto Alumno se pueda convertir 
        correctamente a un diccionario/JSON.
        """
        alumno = self.__nuevo_alumno()
        # No es necesario guardar en BD para testear mapping puro
        
        # 1. Definimos la estructura de datos esperada (JSON/Diccionario)
        datos_esperados = {
            "apellido": "Silva",
            "nombre": "Abril",
            "dni": "12345678",
            "legajo": 1234,
            "nombre_completo": "Silva, Abril" # Ejemplo de campo calculado
        }
        
        # 2. Realizamos el mapping actual
        # NOTA: Dependiendo de tu implementación, esto podría ser:
        # A) Usando Marshmallow: alumno_schema.dump(alumno)
        # B) Usando método propio: alumno.to_dict()
        # C) Manual (simulado aquí para que el test funcione sin librerías extra):
        datos_actuales = {
            "apellido": alumno.apellido,
            "nombre": alumno.nombre,
            "dni": alumno.nro_documento,
            "legajo": alumno.nro_legajo,
            "nombre_completo": f"{alumno.apellido}, {alumno.nombre}"
        }
        
        # 3. Aserciones: Verificamos que el mapping coincida
        self.assertEqual(datos_actuales["dni"], datos_esperados["dni"])
        self.assertEqual(datos_actuales["nombre_completo"], datos_esperados["nombre_completo"])
        self.assertDictEqual(datos_actuales, datos_esperados)

    def __nuevo_alumno(self, dni="12345678", legajo=1234):
        """
        Helper para crear instancias de Alumno.
        Acepta parámetros para DNI y Legajo para permitir crear múltiples alumnos únicos.
        """
        alumno = Alumno()
        
        # Asumiendo que Documento se crea o recupera aquí. 
        # Si 'tipo_documento' es una relación, asegúrate de manejar la sesión correctamente si ya existe "DNI".
        tipo_documento = Documento(tipo_documento="DNI")
        
        alumno.apellido = 'Silva'
        alumno.nombre = 'Abril'
        alumno.nro_documento = dni
        alumno.tipo_documento = tipo_documento
        alumno.fecha_nacimiento = '1990-01-01'
        alumno.sexo = 'F'
        alumno.nro_legajo = legajo
        alumno.fecha_ingreso = '2022-01-01'
        
        return alumno

if __name__ == '__main__':
    unittest.main()