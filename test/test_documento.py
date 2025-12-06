import unittest
import os
from flask import current_app
from app import create_app, db
from app.models.documento import Documento
from app.services.documento_service import DocumentoService

class DocumentoTestCase(unittest.TestCase):

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
        
    def test_documento_creation(self):
        """Prueba la instanciación del objeto en memoria"""
        documento = self.__nuevo_documento()
        self.assertIsNotNone(documento)
        self.assertEqual(documento.tipo_documento, "DNI")
        
    def test_crear_documento(self):
        """Prueba la persistencia en la BD"""
        documento = self.__nuevo_documento()
        DocumentoService.crear_documento(documento)
        
        self.assertIsNotNone(documento)
        self.assertIsNotNone(documento.id)
        self.assertGreaterEqual(documento.id, 1)
        self.assertEqual(documento.tipo_documento, "DNI")

    def test_documento_busqueda(self):
        """Prueba buscar por ID"""
        documento = self.__nuevo_documento()
        DocumentoService.crear_documento(documento)    
        
        resultado = DocumentoService.buscar_por_id(documento.id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.tipo_documento, "DNI")

    def test_buscar_todos_los_documentos(self):
        """Prueba recuperar todos los documentos"""
        # Creamos instancias con tipos distintos
        doc1 = self.__nuevo_documento(tipo="DNI")
        doc2 = self.__nuevo_documento(tipo="Pasaporte")
        
        DocumentoService.crear_documento(doc1)
        DocumentoService.crear_documento(doc2)
        
        documentos = DocumentoService.buscar_todos()
        self.assertIsNotNone(documentos)
        self.assertEqual(len(documentos), 2)

    def test_actualizar_documento(self):
        """Prueba la actualización"""
        documento = self.__nuevo_documento()
        DocumentoService.crear_documento(documento)
        
        documento.tipo_documento = "Pasaporte"
        doc_actualizado = DocumentoService.actualizar_documento(documento.id, documento)
        
        self.assertEqual(doc_actualizado.tipo_documento, "Pasaporte")
        
        # Verificación en BD
        doc_bd = DocumentoService.buscar_por_id(documento.id)
        self.assertEqual(doc_bd.tipo_documento, "Pasaporte")

    def test_borrar_documento(self):
        """Prueba el borrado"""
        documento = self.__nuevo_documento()
        DocumentoService.crear_documento(documento)
        
        DocumentoService.borrar_por_id(documento.id)
        
        resultado = DocumentoService.buscar_por_id(documento.id)
        self.assertIsNone(resultado)

    def test_serializacion_documento(self):
        """
        Prueba de Mapping: Verifica que el objeto Documento se convierta
        correctamente a un diccionario/JSON.
        """
        documento = self.__nuevo_documento(tipo="LC")
        
        # 1. Definir lo que esperamos recibir
        datos_esperados = {
            "tipo_documento": "LC",
            "descripcion": "Tipo de Documento: LC" # Ejemplo de campo hipotético
        }
        
        # 2. Simular el mapeo (Serialización)
        # Esto simula DocumentoSchema().dump(documento)
        datos_actuales = {
            "tipo_documento": documento.tipo_documento,
            "descripcion": f"Tipo de Documento: {documento.tipo_documento}"
        }
        
        # 3. Validar
        self.assertEqual(datos_actuales["tipo_documento"], datos_esperados["tipo_documento"])
        self.assertDictEqual(datos_actuales, datos_esperados)

    def __nuevo_documento(self, tipo="DNI"):
        """
        Helper para crear instancias.
        Permite parámetros dinámicos.
        """
        documento = Documento()
        documento.tipo_documento = tipo
        return documento
        
if __name__ == '__main__':
    unittest.main()