from app.models import Alumno
from app import db
from app.repositories.alumno_repositorio import AlumnoRepository
from app.models.facultad import Facultad
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.repositories.facultad_repositorio import FacultadRepository
import io
import json

class AlumnoService:
    """
    Servicio para gestionar las Alumno.
    """
    @staticmethod
    def crear_alumno(alumno: Alumno):
        """
        Crea una nueva alumno en la base de datos.
        :param alumno: Alumno a crear.
        :return: Alumno creada.
        """
        AlumnoRepository.crear(alumno)
    
    @staticmethod
    def buscar_por_id(id: int) -> Alumno:
        """
        Busca una alumno por su ID.
        :param id: ID de la Alumno a buscar.
        :return: Alumno encontrada o None si no se encuentra.
        """
        return AlumnoRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Alumno]:
        """
        Busca todas las alumno en la base de datos.
        :return: Lista de alumno.
        """
        return AlumnoRepository.buscar_todos()
    
    @staticmethod
    def actualizar_alumno(id: int, alumno: Alumno) -> Alumno:
        """
        Actualiza una alumno existente en la base de datos.
        :param id: ID del alumno a actualizar.
        :param alumno: Objeto Alumno con los nuevos datos.
        :return: Objeto Alumno actualizado o None si no se encuentra.
        """
        alumno_existente = AlumnoRepository.buscar_por_id(id)
        if not alumno_existente:
            return None

        # Transfiere los datos del objeto de entrada al objeto persistente.
        alumno_existente.nombre = alumno.nombre
        alumno_existente.apellido = alumno.apellido
        alumno_existente.nro_legajo = alumno.nro_legajo
        alumno_existente.nro_documento = alumno.nro_documento
        alumno_existente.fecha_nacimiento = alumno.fecha_nacimiento
        alumno_existente.sexo = alumno.sexo
        alumno_existente.fecha_ingreso = alumno.fecha_ingreso
        alumno_existente.tipo_documento_id = alumno.tipo_documento_id
        alumno_existente.facultad_id = alumno.facultad_id

        # Confirma la transacción para guardar los cambios en la base de datos.
        db.session.commit()

        return alumno_existente
    
    @staticmethod
    def generar_pdf(id):
        alumno = AlumnoRepository.buscar_por_id(id)
        if not alumno or not alumno.facultad_id:
            return None  # O manejar el error como prefieras
        facultad = FacultadRepository.buscar_por_id(alumno.facultad_id)

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        c.drawString(100, 750, "Nro de Legajo: " + str(alumno.nro_legajo))
        c.drawString(100, 700, "Apellido y Nombre: " + alumno.apellido + ", " + alumno.nombre)
        c.drawString(100, 650, "Facultad: " + (facultad.nombre if facultad else "N/A"))

        c.save()
        buffer.seek(0)
        return buffer

    @staticmethod
    def borrar_por_id(id: int) -> Alumno:
        """
        Borra una alumno por su ID.
        :param id: ID de la alumno a borrar.
        :return: Objeto Alumno borrado o None si no se encuentra.
        """

        alumno = AlumnoRepository.borrar_por_id(id)
        if not alumno:
            return None
        return alumno