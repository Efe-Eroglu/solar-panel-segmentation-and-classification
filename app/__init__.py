from flask import Flask
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates'),
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')
    )

    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    return app
