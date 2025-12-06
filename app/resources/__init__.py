from flask import Flask 

def init_routes(app: Flask):
    from app.resources.alumno_resources import alumno_bp
    app.register_blueprint(alumno_bp)
    