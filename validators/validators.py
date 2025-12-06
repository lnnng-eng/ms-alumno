from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def validate_with(mapper_class):
    """
    Un decorador para validar el JSON de una petición usando un Mapper.

    Este decorador extrae el JSON del cuerpo de la petición.
    Utiliza el método estático `from_json` del Mapper proporcionado para
    validar los datos y convertirlos en un objeto del modelo.

    - Si la validación es exitosa, el objeto del modelo resultante se pasa
      como un argumento de palabra clave 'data' a la función de la vista.
    - Si no hay JSON en la petición, devuelve un error 400.
    - Si la validación de Marshmallow falla, captura la `ValidationError`
      y devuelve un error 400 con los mensajes de error.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            if not json_data:
                return jsonify({"error": "No se proporcionaron datos de entrada o no es un JSON válido"}), 400
            try:
                kwargs['data'] = mapper_class.from_json(json_data)
            except ValidationError as err:
                return jsonify(err.messages), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator