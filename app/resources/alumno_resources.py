from flask import Blueprint, jsonify, send_file
from app.mapping.alumno_mapping import AlumnoMapper, AlumnoSchema
from app.services.alumno_service import AlumnoService
#from app.validators import validate_with
#from app.models import Alumno
#import logging
#import io

alumno_bp = Blueprint('alumno', __name__)

#pdf
@alumno_bp.route('/alumno/<int:id>/pdf', methods=['GET'])
def get_alumno_pdf(id):
    pdf_buffer = AlumnoService.generar_pdf(id)
    if not pdf_buffer:
        return jsonify({"error": "No se pudo generar el PDF para el alumno o el alumno no fue encontrado"}), 404

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f'alumno_{id}.pdf',
        mimetype='application/pdf'
    )

#buscar
@alumno_bp.route('/alumno/<int:id>', methods=['GET'])
def buscar_por_id(id):
    alumno= AlumnoService.buscar_por_id(id)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return AlumnoSchema().dump(alumno),200

#listar 
@alumno_bp.route('/alumno', methods=['GET'])
def listar_alumnos():
    alumnos = AlumnoService.buscar_todos()
    return AlumnoSchema().dump(alumnos, many=True),200


