from app import db
from app.models import Documento

class DocumentoRepository:
    """
    Repositorio para gestionar las documento.
    """
    @staticmethod
    def crear(documento):
        """
        Crea una nueva documento en la base de datos.
        :param documento: Documento a crear.
        :return: Documento creada.
        """
        db.session.add(documento)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca una documento por su ID.
        :param id: ID de la documento a buscar.
        :return: Documento encontrada o None si no se encuentra.
        """
        return db.session.query(Documento).filter_by(id=id).first() 

    @staticmethod
    def buscar_todos():
        """
        Busca todas las documento en la base de datos.
        :return: Lista de documento.
        """
        return db.session.query(Documento).all()
    
    @staticmethod
    def actualizar_documento(documento) -> Documento:
        """
        Actualiza una documento existente en la base de datos.
        :param id: ID de la documento a actualizar.
        :param documento: Objeto Documento con los nuevos datos.
        :return: Objeto Documento actualizado.
        """
        documento_existente = db.session.merge(documento)
        if not documento_existente:
            return None
        return documento_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Documento:
        """
        Borra una documento por su ID.
        :param id: ID de la documento a borrar.
        :return: Objeto Documento borrado o None si no se encuentra.
        """
        documento = db.session.query(Documento).filter_by(id=id).first()
        if not documento:
            return None
        db.session.delete(documento)
        db.session.commit()
        return documento