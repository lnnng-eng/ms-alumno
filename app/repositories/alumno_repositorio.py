from app import db
from app.models import Alumno

class AlumnoRepository:
    """
    Repositorio para gestionar las alumno.
    """
    @staticmethod
    def crear(alumno):
        """
        Crea una nueva alumno en la base de datos.
        :param alumno: Alumno a crear.
        :return: Alumno creada.
        """
        db.session.add(alumno)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca una alumno por su ID.
        :param id: ID de la alumno a buscar.
        :return: Alumno encontrada o None si no se encuentra.
        """
        return db.session.query(Alumno).filter_by(id=id).first() 

    @staticmethod
    def buscar_todos():
        """
        Busca todas las alumno en la base de datos.
        :return: Lista de alumno.
        """
        return db.session.query(Alumno).all()
    
    @staticmethod
    def actualizar_alumno(alumno) -> Alumno:
        """
        Actualiza una alumno existente en la base de datos.
        :param id: ID de la alumno a actualizar.
        :param alumno: Objeto Alumno con los nuevos datos.
        :return: Objeto Alumno actualizado.
        """
        alumno_existente = db.session.merge(alumno)
        if not alumno_existente:
            return None
        return alumno_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Alumno:
        """
        Borra una alumno por su ID.
        :param id: ID de la alumno a borrar.
        :return: Objeto Alumno borrado o None si no se encuentra.
        """
        alumno = db.session.query(Alumno).filter_by(id=id).first()
        if not alumno:
            return None
        db.session.delete(alumno)
        db.session.commit()
        return alumno