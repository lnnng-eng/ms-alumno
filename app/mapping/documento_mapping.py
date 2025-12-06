from marshmallow import Schema, fields, post_load, EXCLUDE
from app.models.documento import Documento

class DocumentoSchema(Schema):
    class Meta:
        # Ignora campos desconocidos que vengan en el JSON
        unknown = EXCLUDE 

    # Mapeamos 'code' del JSON al 'id' de la entidad
    # En tablas maestras, a veces sí queremos forzar el ID para mantener consistencia entre servicios
    id = fields.Int(required=True, data_key="code")
    
    # Mapeamos 'description' a 'tipo_documento'
    tipo_documento = fields.Str(required=True, data_key="description")

    @post_load
    def make_documento(self, data, **kwargs):
        # SQLAlchemy permite constructor con kwargs aunque tengas init=False
        return Documento(**data)

class DocumentoMapper:
    @staticmethod
    def from_json(json_data: dict) -> Documento:
        schema = DocumentoSchema()
        return schema.load(json_data)

    @staticmethod
    def to_json(documento: Documento) -> dict:
        schema = DocumentoSchema()
        return schema.dump(documento)