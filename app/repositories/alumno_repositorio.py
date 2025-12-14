from app import db
from app.models import Alumno

class AlumnoRepository:
    """
    Repositorio para gestionar las alumno.
    """

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Alumno).filter_by(id=id).first() 

    @staticmethod
    def buscar_todos():
        return db.session.query(Alumno).all()
    
    