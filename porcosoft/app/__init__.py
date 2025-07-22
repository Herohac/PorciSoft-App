from flask import Flask
from flask_cors import CORS # <--- 1. IMPORTA LA LIBRERÍA

def create_app():
    app = Flask(__name__)
    CORS(app) # <--- 2. APLICA CORS A TU APP

    with app.app_context():
        # Aquí registraremos nuestras rutas más adelante
        from . import routes

    return app