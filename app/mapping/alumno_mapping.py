from marshmallow import Schema, fields


class AlumnoSchema(Schema):
    id = fields.Int(dump_only=True) 
    nombre = fields.String()
    apellido = fields.String()
    nro_documento = fields.String()
    nro_legajo = fields.Integer()
    
#no @post_load, No logica solo mapping  
    
    
    
