from app.models import Alumno
from app import db
from app.repositories.alumno_repositorio import AlumnoRepository
from reportlab.pdfgen import canvas
import io
import json

class AlumnoService:
    """
    Servicio para gestionar las Alumno.
    """
    
    @staticmethod
    def buscar_por_id(id: int) -> Alumno:
        return AlumnoRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Alumno]:
        return AlumnoRepository.buscar_todos()
    
    @staticmethod
    def generar_pdf(id):
        alumno = AlumnoRepository.buscar_por_id(id)
        if not alumno:
            return None 

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer)

        c.drawString(100, 750, f"Legajo: {alumno.nro_legajo}")
        c.drawString(100, 700, f"Alumno: {alumno.apellido}, {alumno.nombre}")
        
        c.save()
        buffer.seek(0)
        return buffer

#nada de crear, actualizar, borrar
