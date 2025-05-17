from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuración para subida de archivos
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'img')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Límite de 16MB
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Crear carpeta si no existe

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from app.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app