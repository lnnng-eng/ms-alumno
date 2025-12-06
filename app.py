from app import app # Se importa la instancia 'app' directamente desde el paquete.
import logging
# Ref: https://docs.python.org/3/library/logging.html
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

if __name__ == '__main__':
    """
    Server Startup
    Ref: https://flask.palletsprojects.com/en/stable/api/#flask.Flask.run
    Ref: Book Flask Web Development Page 9
    """
    app.run(host="0.0.0.0", debug=False, port=5000)
    