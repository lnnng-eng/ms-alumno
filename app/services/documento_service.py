from app.models import Documento
from app.repositories.documento_repositorio import DocumentoRepository

class DocumentoService:
    """
    Servicio para gestionar las documento.
    """
    @staticmethod
    def crear_documento(documento: Documento):
        """
        Crea una nueva documento en la base de datos.
        :param documento: Documento a crear.
        :return: Documento creada.
        """
        DocumentoRepository.crear(documento)
    
    @staticmethod
    def buscar_por_id(id: int) -> Documento:
        """
        Busca una documento por su ID.
        :param id: ID de la documento a buscar.
        :return: Documento encontrada o None si no se encuentra.
        """
        return DocumentoRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Documento]:
        """
        Busca todas las documento en la base de datos.
        :return: Lista de documento.
        """
        return DocumentoRepository.buscar_todos()
    
    @staticmethod
    def actualizar_documento(id: int, documento: Documento) -> Documento:
        """
        Actualiza una documento existente en la base de datos.
        :param id: ID de la documento a actualizar.
        :param documento: Objeto Documento con los nuevos datos.
        :return: Objeto Documento actualizada.
        """
        documento_existente = DocumentoRepository.buscar_por_id(id)
        if not documento_existente:
            return None
        documento_existente.tipo_documento = documento.tipo_documento
        return documento_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Documento:
        """
        Borra una documento por su ID.
        :param id: ID de la documento a borrar.
        :return: Objeto Documento borrado o None si no se encuentra.
        """

        documento = DocumentoRepository.borrar_por_id(id)
        if not documento:
            return None
        return documento