from marshmallow import Schema, fields, post_load, validate, EXCLUDE
from app.models.facultad import Facultad

class FacultadSchema(Schema):
    class Meta:
        # Si el microservicio agrega campos nuevos en el futuro, no rompemos la app
        unknown = EXCLUDE

    # --- Identificadores ---
    id = fields.Int(dump_only=True) # Generalmente no insertamos el ID, lo genera la DB
    
    # --- Datos Principales ---
    # data_key conecta el JSON 'facultyName' con el modelo 'nombre'
    nombre = fields.Str(required=True, data_key="facultyName", validate=validate.Length(max=100))
    abreviatura = fields.Str(required=True, data_key="shortName", validate=validate.Length(max=10))
    sigla = fields.Str(required=True, data_key="acronym", validate=validate.Length(max=10))
    directorio = fields.Str(required=True, data_key="path", validate=validate.Length(max=100))
    
    # --- Ubicación (Opcionales en DB, pero quizás requeridos en el mapping si lo deseas) ---
    codigo_postal = fields.Str(allow_none=True, data_key="zipCode", validate=validate.Length(max=10))
    ciudad = fields.Str(allow_none=True, validate=validate.Length(max=50))
    domicilio = fields.Str(allow_none=True, data_key="address", validate=validate.Length(max=100))
    
    # --- Contacto ---
    telefono = fields.Str(allow_none=True, data_key="phoneNumber", validate=validate.Length(max=20))
    contacto = fields.Str(allow_none=True, data_key="contactPerson", validate=validate.Length(max=100))
    
    # Validación automática de formato de email
    email = fields.Email(required=True, data_key="emailAddress", validate=validate.Length(max=100))

    @post_load
    def make_facultad(self, data, **kwargs):
        """
        Convierte el diccionario validado en una instancia de Facultad.
        """
        return Facultad(**data)

class FacultadMapper:
    @staticmethod
    def from_json(json_data: dict) -> Facultad:
        schema = FacultadSchema()
        return schema.load(json_data)

    @staticmethod
    def to_json(facultad: Facultad) -> dict:
        """
        Útil si tu Flask app también expone estos datos a un Frontend
        """
        schema = FacultadSchema()
        return schema.dump(facultad)